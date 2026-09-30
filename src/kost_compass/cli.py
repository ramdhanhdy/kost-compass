"""Small, reproducible command-line interface."""

import argparse
import json
from pathlib import Path

from .ranking import assess_listing, validate_constraints


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='kost-compass')
    sub = parser.add_subparsers(dest='command', required=True)
    rank = sub.add_parser('rank', help='Calculate exact monthly budget flags and straight-line distances')
    rank.add_argument('--input', type=Path, required=True)
    rank.add_argument('--target-lat', type=float, required=True)
    rank.add_argument('--target-lon', type=float, required=True)
    rank.add_argument('--budget', type=int, required=True)
    rank.add_argument('--max-distance', type=float)
    args = parser.parse_args(argv)
    try:
        validate_constraints((args.target_lat, args.target_lon), args.budget, args.max_distance)
        data = json.loads(args.input.read_text())
        if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
            raise ValueError('Input must be a JSON array of listing objects')
        rows = [assess_listing(row, (args.target_lat, args.target_lon), args.budget, args.max_distance)
                for row in data]
        priority = {'within_budget': 0, 'unknown': 1, 'over_budget': 2}
        rows.sort(key=lambda row: (priority[row['budget_status']],
                                  row['distance_km'] if row['distance_km'] is not None else float('inf')))
        print(json.dumps({'count': len(rows), 'budget_idr': args.budget,
                          'target': [args.target_lat, args.target_lon], 'rows': rows},
                         ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (ValueError, OSError) as error:
        parser.error(str(error))
        return 2
