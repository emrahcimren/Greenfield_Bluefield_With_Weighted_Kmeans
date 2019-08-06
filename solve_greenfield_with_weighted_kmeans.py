'''
Function to solve greenfield with weighted k-means
'''

import pandas as pd
from src import ini
from src import weighted_kmeans_algorithm as wka


def solve_greenfield_with_weighted_kmeans():
    inputs = ini.IniInput('inputs.ini')
    number_of_clusters_list = range(inputs.minimum_number_of_clusters, inputs.maximum_number_of_clusters)

    all_clusters = []
    all_customers_with_clusters = []
    for number_of_clusters in number_of_clusters_list:
        print('Running for {} Number of Clusters'.format(str(number_of_clusters)))

        minimum_elements_in_a_cluster = round(
            inputs.minimum_elements_in_a_cluster_ratio * len(inputs.customers) / number_of_clusters)
        maximum_elements_in_a_cluster = round(
            inputs.maximum_elements_in_a_cluster_ratio * len(inputs.customers) / number_of_clusters)

        clusters, customers_with_clusters = wka.run_weighted_kmeans_algorithm(inputs.customers, number_of_clusters,
                                                                              minimum_elements_in_a_cluster,
                                                                              maximum_elements_in_a_cluster,
                                                                              inputs.objective_range,
                                                                              inputs.max_iterations)
        clusters['NUMBER_OF_CLUSTERS'] = number_of_clusters
        customers_with_clusters['NUMBER_OF_CLUSTERS'] = number_of_clusters

        all_clusters.append(clusters)
        all_customers_with_clusters.append(customers_with_clusters)

    all_clusters = pd.concat(all_clusters)
    all_customers_with_clusters = pd.concat(all_customers_with_clusters)

    all_clusters.to_csv('data/results/clusters.csv', index=False)
    all_customers_with_clusters.to_csv('data/results/customers_with_clusters.csv', index=False)
