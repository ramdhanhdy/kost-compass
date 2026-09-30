"""Straight-line distances only; never pretend these are walking routes."""

import math


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    for value, limit in ((lat1, 90), (lat2, 90), (lon1, 180), (lon2, 180)):
        if type(value) not in (int, float) or not math.isfinite(value) or abs(value) > limit:
            raise ValueError('Coordinates must be finite numeric degrees within geographic bounds')
    a, b = math.radians(lat1), math.radians(lat2)
    delta_lat = b - a
    delta_lon = math.radians(lon2 - lon1)
    h = math.sin(delta_lat / 2) ** 2 + math.cos(a) * math.cos(b) * math.sin(delta_lon / 2) ** 2
    return 6371.0088 * 2 * math.asin(min(1.0, math.sqrt(h)))
