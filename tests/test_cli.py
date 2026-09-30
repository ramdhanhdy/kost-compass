import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class CLITests(unittest.TestCase):
    def test_rank_command_returns_exact_budget_flags_and_distances(self):
        # Deliberately synthetic unit-test records, not claimed housing data.
        records = [
            {'name': 'unit-test-only near', 'source_url': 'https://example.invalid/test/1',
             'price_idr': 2400000, 'price_period': 'month', 'latitude': 0.0,
             'longitude': 0.01, 'coordinate_precision': 'property'},
            {'name': 'unit-test-only over', 'source_url': 'https://example.invalid/test/2',
             'price_idr': 2400001, 'price_period': 'month'},
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'records.json'
            path.write_text(json.dumps(records))
            result = subprocess.run([sys.executable, '-m', 'kost_compass', 'rank',
                                     '--input', str(path), '--target-lat', '0', '--target-lon', '0',
                                     '--budget', '2400000', '--max-distance', '3'],
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data['count'], 2)
            self.assertEqual(data['rows'][0]['budget_status'], 'within_budget')
            self.assertEqual(data['rows'][0]['proximity_status'], 'within_radius')
            self.assertEqual(data['rows'][1]['budget_status'], 'over_budget')

    def test_empty_input_rejects_invalid_constraints(self):
        cases = [
            ('--budget', '-1', 'Budget must be a nonnegative integer amount in IDR'),
            ('--max-distance', '-1', 'Radius must be finite and nonnegative'),
            ('--max-distance', 'nan', 'Radius must be finite and nonnegative'),
            ('--max-distance', 'inf', 'Radius must be finite and nonnegative'),
            ('--target-lat', '91', 'Coordinates must be finite numeric degrees within geographic bounds'),
            ('--target-lon', '181', 'Coordinates must be finite numeric degrees within geographic bounds'),
            ('--target-lat', 'nan', 'Coordinates must be finite numeric degrees within geographic bounds'),
            ('--target-lon', 'inf', 'Coordinates must be finite numeric degrees within geographic bounds'),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'records.json'
            path.write_text('[]')
            for option, value, message in cases:
                with self.subTest(option=option, value=value):
                    constraints = {'--target-lat': '0', '--target-lon': '0', '--budget': '2400000'}
                    constraints[option] = value
                    result = subprocess.run(
                        [sys.executable, '-m', 'kost_compass', 'rank', '--input', str(path),
                         *[f'{key}={value}' for key, value in constraints.items()]],
                        text=True, capture_output=True)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertEqual(result.stdout, '')
                    self.assertIn(message, result.stderr)


if __name__ == '__main__':
    unittest.main()
