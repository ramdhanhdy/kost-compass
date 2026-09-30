import importlib
import unittest

try:
    ranking = importlib.import_module('kost_compass.ranking')
except ModuleNotFoundError:
    ranking = None


class BudgetTests(unittest.TestCase):
    def test_only_explicit_monthly_rent_is_compared_at_inclusive_cap(self):
        self.assertIsNotNone(ranking, 'Ranking implementation is missing')
        assert ranking is not None
        target = (-6.2374409, 106.798634)
        row = {'name': 'Unit-test listing', 'price_idr': 2400000, 'price_period': 'month'}
        self.assertEqual(ranking.assess_listing(row, target, 2400000)['budget_status'], 'within_budget')
        row['price_idr'] = 2400001
        self.assertEqual(ranking.assess_listing(row, target, 2400000)['budget_status'], 'over_budget')
        row['price_period'] = 'year'
        self.assertEqual(ranking.assess_listing(row, target, 2400000)['budget_status'], 'unknown')
        row['price_period'] = 'month'
        row['price_idr'] = None
        self.assertEqual(ranking.assess_listing(row, target, 2400000)['budget_status'], 'unknown')


    def test_published_point_is_ranked_but_area_geocode_stays_review_only(self):
        assert ranking is not None
        target = (0.0, 0.0)
        row = {'price_idr': 2000000, 'price_period': 'month',
               'latitude': 0.0, 'longitude': 0.01, 'coordinate_precision': 'property'}
        result = ranking.assess_listing(row, target, 2400000, 3.0)
        self.assertIsNotNone(result['distance_km'])
        self.assertEqual(result['proximity_status'], 'within_radius')
        row['longitude'] = 1.0
        self.assertEqual(ranking.assess_listing(row, target, 2400000, 3.0)['proximity_status'], 'outside_radius')
        row['coordinate_precision'] = 'area'
        self.assertEqual(ranking.assess_listing(row, target, 2400000, 3.0)['proximity_status'], 'unknown')


    def test_invalid_budget_radius_and_target_fail_closed(self):
        assert ranking is not None
        for kwargs in [{'budget_idr': -1}, {'budget_idr': True},
                       {'max_distance_km': -1}, {'max_distance_km': float('nan')},
                       {'target': (100, 0)}]:
            args = {'listing': {}, 'target': (0, 0), 'budget_idr': 2400000}
            args.update(kwargs)
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                ranking.assess_listing(**args)


    def test_absent_radius_does_not_invent_a_proximity_limit(self):
        assert ranking is not None
        row = {'latitude': 0, 'longitude': 0.01, 'coordinate_precision': 'property'}
        result = ranking.assess_listing(row, (0, 0), 2400000)
        self.assertEqual(result['proximity_status'], 'not_limited')

if __name__ == '__main__':
    unittest.main()
