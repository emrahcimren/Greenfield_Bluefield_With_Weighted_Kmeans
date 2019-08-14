'''
File to implement weighted KMeans algorithm
'''

import pandas as pd
from src import haversine_distance
from src import depo_customer_allocation_or_tools_model as ort


def __calculate_cluster_centers(customers_at_iteration_with_clusters):
    '''
    Calculate cluster centers
    :param customers_at_iteration_with_clusters:
    :return: clusters with lat and lon
    '''

    clusters = customers_at_iteration_with_clusters.groupby(['CLUSTER'], as_index=False).agg(
        {'LATITUDE': 'sum', 'LONGITUDE': 'sum',
         'CUSTOMER_NAME': 'count'}).rename(
        columns={'LATITUDE': 'CLUSTER_LATITUDE', 'LONGITUDE': 'CLUSTER_LONGITUDE',
                 'CUSTOMER_NAME': 'NUMBER_OF_CUSTOMERS_IN_A_CLUSTER'})

    clusters['CLUSTER_LATITUDE'] = clusters['CLUSTER_LATITUDE'] / clusters['NUMBER_OF_CUSTOMERS_IN_A_CLUSTER']
    clusters['CLUSTER_LONGITUDE'] = clusters['CLUSTER_LONGITUDE'] / clusters['NUMBER_OF_CUSTOMERS_IN_A_CLUSTER']

    return clusters


def __calculate_weighted_distance(customers_at_iteration_with_clusters):
    distance = haversine_distance.calculate_haversine_distance(customers_at_iteration_with_clusters['LATITUDE'],
                                                               customers_at_iteration_with_clusters['LONGITUDE'],
                                                               customers_at_iteration_with_clusters['CLUSTER_LATITUDE'],
                                                               customers_at_iteration_with_clusters[
                                                                   'CLUSTER_LONGITUDE'])
    customers_at_iteration_with_clusters['DISTANCE'] = distance
    customers_at_iteration_with_clusters['WEIGHTED_DISTANCE'] = customers_at_iteration_with_clusters['DISTANCE'] * \
                                                                customers_at_iteration_with_clusters['DEMAND']
    customers_at_iteration_with_clusters.drop(['DISTANCE'], 1, inplace=True)

    return customers_at_iteration_with_clusters


def __initiate_weighted_kmeans_algorithm(iteration, customers_at_iteration_with_clusters, number_of_clusters):
    # randomly assign customers to K clusters
    clusters = list(range(0, number_of_clusters)) * round(
        len(customers_at_iteration_with_clusters) / number_of_clusters + 1)
    clusters = clusters[:len(customers_at_iteration_with_clusters)]
    customers_at_iteration_with_clusters['CLUSTER'] = clusters

    clusters = __calculate_cluster_centers(customers_at_iteration_with_clusters)
    customers_at_iteration_with_clusters = customers_at_iteration_with_clusters.merge(clusters, how='left',
                                                                                      on='CLUSTER')

    customers_at_iteration_with_clusters = __calculate_weighted_distance(customers_at_iteration_with_clusters)
    customers_at_iteration_with_clusters['ITERATION'] = iteration

    objective = customers_at_iteration_with_clusters['WEIGHTED_DISTANCE'].sum().round(2)
    customers_at_iteration_with_clusters['OBJECTIVE'] = objective

    return objective, clusters, customers_at_iteration_with_clusters


def __calculate_distance_matrix(customers_at_iteration, clusters_for_distance):
    customers_at_iteration['Key'] = 0
    clusters_for_distance['Key'] = 0
    customers_at_iteration_with_clusters = customers_at_iteration.merge(clusters_for_distance)
    customers_at_iteration_with_clusters = __calculate_weighted_distance(customers_at_iteration_with_clusters)

    return customers_at_iteration_with_clusters[['CUSTOMER_NAME', 'CLUSTER', 'WEIGHTED_DISTANCE']]


def run_weighted_kmeans_algorithm(customers, number_of_clusters, minimum_elements_in_a_cluster,
                                  maximum_elements_in_a_cluster, objective_range, max_iteration):
    all_clusters = []
    all_customers_with_clusters = []

    iteration = 0
    print('Running iteration {}'.format(str(iteration)))
    prev_objective, prev_clusters, prev_customers_at_iteration_with_clusters = __initiate_weighted_kmeans_algorithm(
        iteration, customers.copy(), number_of_clusters)
    prev_clusters['ITERATION'] = iteration
    prev_customers_at_iteration_with_clusters['SOLUTION'] = 0

    all_clusters.append(prev_clusters)
    all_customers_with_clusters.append(prev_customers_at_iteration_with_clusters)

    solution_not_found = True
    while solution_not_found:
        print('Running iteration {}'.format(str(iteration)))

        customer_cluster_distance_matrix = __calculate_distance_matrix(customers.copy(), prev_clusters)
        solution = ort.formulate_and_solve_ortools_model(customer_cluster_distance_matrix,
                                                         minimum_elements_in_a_cluster,
                                                         maximum_elements_in_a_cluster)

        if len(solution) > 0:
            print('Optimal solution is found')
            iteration = iteration + 1

            solution['ITERATION'] = iteration

            objective = round(solution['WEIGHTED_DISTANCE'].sum(), 2)
            solution['OBJECTIVE'] = objective

            customers_at_iteration_with_clusters = customers.copy().merge(solution, how='left', on=['CUSTOMER_NAME'])
            clusters = __calculate_cluster_centers(customers_at_iteration_with_clusters)
            clusters['ITERATION'] = iteration

            customers_at_iteration_with_clusters = customers_at_iteration_with_clusters.merge(clusters, how='left',
                                                                                              on=['CLUSTER'])
            customers_at_iteration_with_clusters['ITERATION'] = iteration
            customers_at_iteration_with_clusters['SOLUTION'] = 0

            customers_at_iteration_with_clusters = customers_at_iteration_with_clusters[
                prev_customers_at_iteration_with_clusters.columns]

            print('Current objective {}'.format(str(objective)))
            print('Prev objective {}'.format(str(prev_objective)))

            if abs(objective - prev_objective) < objective_range:
                print('Solution found')
                solution_not_found = False
                prev_customers_at_iteration_with_clusters['SOLUTION'] = 1

            elif (prev_objective < objective) and iteration > max_iteration:
                print('Stopping')
                solution_not_found = False
                prev_customers_at_iteration_with_clusters['SOLUTION'] = 1

            else:
                prev_objective = objective
                prev_clusters = clusters
                prev_customers_at_iteration_with_clusters = customers_at_iteration_with_clusters

                all_clusters.append(prev_clusters)
                all_customers_with_clusters.append(prev_customers_at_iteration_with_clusters)

    return pd.concat(all_clusters), pd.concat(all_customers_with_clusters)
