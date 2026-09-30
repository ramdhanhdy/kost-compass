import importlib
import math
import unittest

try:
    geo = importlib.import_module('kost_compass.geo')
except ModuleNotFoundError:
    geo = None


class DistanceTests(unittest.TestCase):
    def test_haversine_same_point_is_zero_and_equator_degree_is_known(self):
        self.assertIsNotNone(geo, 'Geospatial implementation does not exist yet')
        self.assertEqual(geo.haversine_km(0, 0, 0, 0), 0)
        self.assertAlmostEqual(geo.haversine_km(0, 0, 0, 1), 111.195, places=3)


    def test_rejects_invalid_or_nonfinite_coordinates(self):
        assert geo is not None
        for coords in [(91, 0, 0, 0), (0, 181, 0, 0), (math.nan, 0, 0, 0), (True, 0, 0, 0)]:
            with self.subTest(coords=coords), self.assertRaises(ValueError):
                geo.haversine_km(*coords)


if __name__ == '__main__':
    unittest.main()
