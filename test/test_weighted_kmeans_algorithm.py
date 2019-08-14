'''
Test class for the weighted kmeans algorithm
'''

import unittest
import pandas as pd
from src import weighted_kmeans_algorithm as wkm


class WeightedKmeansTest(unittest.TestCase):

    def set_up(self):

        self.customers = pd.DataFrame({'CUSTOMER_NAME': ['Customer 7', 'Customer 8', 'Customer 6', 'Customer 9'],
                                  'LATITUDE': [49.54617, 50.48072, 49.756845, 49.68722],
                                  'LONGITUDE': [4.791979253, 2.410053869, 4.007695426, 3.792182567],
                                  'DEMAND': [1802, 4044, 2392, 4868]
                                  })

        self.number_of_clusters = 2
        self.minimum_elements_in_a_cluster = 1
        self.maximum_elements_in_a_cluster = 2
        self.objective_range = 0.001
        self.max_iteration = 10

    def test_run_weighted_kmeans_algorithm(self):

        self.set_up()
        all_clusters, all_customers_with_clusters = wkm.run_weighted_kmeans_algorithm(self.customers,
                                                                                      self.number_of_clusters,
                                                                                      self.minimum_elements_in_a_cluster,
                                                                                      self.maximum_elements_in_a_cluster,
                                                                                      self.objective_range,
                                                                                      self.max_iteration)

        self.assertTrue(len(all_customers_with_clusters) > 0)


if __name__ == '__main__':
    unittest.main()
