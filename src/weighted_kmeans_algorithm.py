

def __calculate_cluster_centers(customers_at_iteration_with_clusters):

    '''
    Calculate cluster centers
    :param customers_at_iteration_with_clusters:
    :return: clusters with lat and lon
    '''

    clusters = customers_at_iteration_with_clusters.groupby(['CLUSTER'], as_index=False).agg({'LATITUDE': 'sum', 'LONGITUDE': 'sum',
                                                                       'CUSTOMER_NAME': 'count'}).rename(
        columns={'LATITUDE': 'CLUSTER_LATITUDE', 'LONGITUDE': 'CLUSTER_LONGITUDE', 'CUSTOMER_NAME': 'NUMBER_OF_CUSTOMERS_IN_A_CLUSTER'})

    clusters['CLUSTER_LATITUDE'] = clusters['CLUSTER_LATITUDE'] / clusters['NUMBER_OF_CUSTOMERS_IN_A_CLUSTER']
    clusters['CLUSTER_LONGITUDE'] = clusters['CLUSTER_LONGITUDE'] / clusters['NUMBER_OF_CUSTOMERS_IN_A_CLUSTER']

    return clusters


def __initiate_weighted_kmeans_algorithm(customers, number_of_clusters):

    #randomly assign stores to K clusters
    iteration = 0
    print('Running iteration {}'.format(str(iteration)))

    # randomly assign clusters #
    customers_at_iteration_with_clusters = customers.copy()
    clusters = list(range(0, number_of_clusters))*round(len(customers_at_iteration_with_clusters)/number_of_clusters+1)
    clusters = clusters[:len(customers_at_iteration_with_clusters)]
    customers_at_iteration_with_clusters['CLUSTER'] = clusters

    clusters = __calculate_cluster_centers(customers_at_iteration_with_clusters)
    customers_at_iteration_with_clusters = customers_at_iteration_with_clusters.merge(clusters, how='left', on='CLUSTER')



    cluster, store_location = calculate_clusters_and_distance(store_location)
    print(cluster)
    store_location['ITERATION'] = iteration
    objective = round(store_location['WEIGHTED_DISTANCE'].sum(), 2)

    prev_objective = objective
    prev_store_location = store_location.copy()



def run_weighted_kmeans_algorithm(customers, number_of_clusters, minimum_elements_in_a_cluster, maximum_elements_in_a_cluster):



