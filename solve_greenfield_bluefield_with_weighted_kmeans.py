'''
Function to solve greenfield with weighted k-means
'''

import pandas as pd
import logging
from src import ini
from src import logger
from src import weighted_kmeans_algorithm as wka


def solve_greenfield_bluefield_with_weighted_kmeans():
    '''
    Solve greenfield, brownfield, or bluefield problem
    :return: csvs saved to data/results_greenfield_bluefield folder
    '''

    inputs = ini.IniInput('inputs.ini')
    logger.set_logger(inputs.run_id)

    number_of_clusters_list = range(inputs.minimum_number_of_clusters, inputs.maximum_number_of_clusters)
    initial_cluster = wka.create_initial_clusters(inputs.use_current_clusters, inputs.current_clusters)

    all_clusters = []
    all_customers_with_clusters = []
    for number_of_clusters in number_of_clusters_list:

        logging.info('Running for {} Number of Clusters'.format(str(number_of_clusters)))

        minimum_elements_in_a_cluster = round(
            inputs.minimum_elements_in_a_cluster_ratio * len(inputs.customers) / number_of_clusters)
        maximum_elements_in_a_cluster = round(
            inputs.maximum_elements_in_a_cluster_ratio * len(inputs.customers) / number_of_clusters)

        logging.info('Minimum elements in a cluster = {}'.format(str(minimum_elements_in_a_cluster)))
        logging.info('Maximum elements in a cluster = {}'.format(str(maximum_elements_in_a_cluster)))

        clusters = wka.initiate_clusters(initial_cluster, number_of_clusters)

        clusters, customers_with_clusters = wka.run_weighted_kmeans_algorithm(inputs.customers, clusters,
                                                                              number_of_clusters,
                                                                              minimum_elements_in_a_cluster,
                                                                              maximum_elements_in_a_cluster,
                                                                              inputs.objective_range,
                                                                              inputs.max_iterations,
                                                                              inputs.enable_minimum_maximum_elements_in_a_cluster)
        clusters['NUMBER_OF_CLUSTERS'] = number_of_clusters
        customers_with_clusters['NUMBER_OF_CLUSTERS'] = number_of_clusters

        all_clusters.append(clusters)
        all_customers_with_clusters.append(customers_with_clusters)

    all_clusters = pd.concat(all_clusters)
    all_customers_with_clusters = pd.concat(all_customers_with_clusters)

    all_clusters.to_csv('data/results_greenfield_bluefield/clusters_unk.csv', index=False)
    all_customers_with_clusters.to_csv('data/results_greenfield_bluefield/customers_with_clusters.csv', index=False)


if __name__ == '__main__':
    solve_greenfield_bluefield_with_weighted_kmeans()
