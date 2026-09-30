"""Exact cost limits belong in code, not model judgments."""


from .geo import haversine_km


def validate_constraints(target: tuple[float, float], budget_idr: int,
                         max_distance_km: float | None = None) -> None:
    import math

    if type(budget_idr) is not int or budget_idr < 0:
        raise ValueError('Budget must be a nonnegative integer amount in IDR')
    if max_distance_km is not None and (type(max_distance_km) not in (int, float)
                                        or not math.isfinite(max_distance_km) or max_distance_km < 0):
        raise ValueError('Radius must be finite and nonnegative')
    haversine_km(target[0], target[1], target[0], target[1])


def assess_listing(listing: dict, target: tuple[float, float], budget_idr: int,
                   max_distance_km: float | None = None) -> dict:
    validate_constraints(target, budget_idr, max_distance_km)
    result = dict(listing)
    price = listing.get('price_idr')
    monthly = listing.get('price_period') == 'month'
    if monthly and isinstance(price, int) and not isinstance(price, bool) and price > 0:
        result['budget_status'] = 'within_budget' if price <= budget_idr else 'over_budget'
    else:
        result['budget_status'] = 'unknown'
    result['distance_km'] = None
    result['distance_kind'] = 'straight_line'
    result['proximity_status'] = 'unknown'
    lat, lon = listing.get('latitude'), listing.get('longitude')
    if lat is not None and lon is not None:
        result['distance_km'] = haversine_km(target[0], target[1], lat, lon)
        if listing.get('coordinate_precision') in ('property', 'address'):
            result['proximity_status'] = 'not_limited' if max_distance_km is None else 'within_radius'
            if max_distance_km is not None and result['distance_km'] > max_distance_km:
                result['proximity_status'] = 'outside_radius'
    return result
