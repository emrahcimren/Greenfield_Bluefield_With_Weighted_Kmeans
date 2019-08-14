'''
Test class for the weighted kmeans algorithm
'''

import unittest
import pandas as pd
from src import depot_customer_allocation_or_tools_model as dc


class DepotCustomerAllocationTest(unittest.TestCase):

    def set_up(self):
        self.customer_cluster_distance_matrix = pd.DataFrame({'CLUSTER': ['1', '1', '1', '1',
                                                                          '2', '2', '2', '2'],
                                                              'CUSTOMER_NAME': ['Customer 7', 'Customer 8',
                                                                                'Customer 6', 'Customer 9',
                                                                                'Customer 7', 'Customer 8',
                                                                                'Customer 6', 'Customer 9'],
                                                              'WEIGHTED_DISTANCE': [10, 15, 20, 25, 8, 4, 5, 5]})

        self.minimum_elements_in_a_cluster = 1
        self.maximum_elements_in_a_cluster = 2

    def test_run_weighted_kmeans_algorithm(self):

        self.set_up()
        solution = dc.formulate_and_solve_ortools_model(self.customer_cluster_distance_matrix,
                                                        self.minimum_elements_in_a_cluster,
                                                        self.maximum_elements_in_a_cluster)

        self.assertAlmostEqual(solution['WEIGHTED_DISTANCE'].sum(), 35)


if __name__ == '__main__':
    unittest.main()
