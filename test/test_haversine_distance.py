'''
Test class for Haversine calculations
'''

import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
from src import haversine_distance as hd


class HaversineDistanceTest(unittest.TestCase):

    def set_up(self):

        self.from_latitude = [49.54617, 50.48072]
        self.from_longitude = [4.791979253, 2.410053869]

        self.to_latitude = [50.81732, 49.298095]
        self.to_longitude = [4.763345862, 4.803297067]

    def test_calculate_haversine_distance(self):

        self.set_up()
        distances = hd.calculate_haversine_distance(self.from_latitude, self.from_longitude, self.to_latitude, self.to_longitude)

        self.assertAlmostEqual(distances[0], 102.77576035)


if __name__ == '__main__':
    unittest.main()
