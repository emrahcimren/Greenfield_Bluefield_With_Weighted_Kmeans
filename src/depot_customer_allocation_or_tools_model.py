'''
Formulate and solve depot-customer allocation model
'''

import logging
import pandas as pd
import collections
from ortools.linear_solver import pywraplp


def __prepare_model_inputs(customer_cluster_distance_matrix):

    logging.info('Getting model inputs')

    DistanceInputs = collections.namedtuple('DistanceInputs', ['DISTANCE', 'WEIGHTED_DISTANCE'])
    distance = {}
    for row in customer_cluster_distance_matrix.itertuples():
        distance[row.CLUSTER, row.CUSTOMER_NAME] = (DistanceInputs(
            DISTANCE=row.DISTANCE,
            WEIGHTED_DISTANCE=row.WEIGHTED_DISTANCE))

    customer_list = []
    cluster_list = []
    for cluster, customer in distance.keys():
        cluster_list.append(cluster)
        customer_list.append(customer)
    customer_list = list(dict.fromkeys(customer_list))
    cluster_list = list(dict.fromkeys(cluster_list))

    return customer_list, cluster_list, distance


def formulate_and_solve_ortools_model(customer_cluster_distance_matrix,
                                      minimum_elements_in_a_cluster,
                                      maximum_elements_in_a_cluster,
                                      enable_minimum_maximum_elements_in_a_cluster):

    logging.info('Formulating the optimization model')
    customer_list, cluster_list, distance = __prepare_model_inputs(customer_cluster_distance_matrix)

    # formulate model
    solver = pywraplp.Solver('SolveIntegerProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # create variables #
    logging.info('create variables')
    y = {}
    for cluster, customer in distance.keys():
        y[cluster, customer] = solver.BoolVar('y[cluster = {}, {}]'.format(str(cluster), customer))

    # Add constraints
    logging.info('each store is assigned to one cluster')
    # each store is assigned to one cluster
    for customer in customer_list:
        solver.Add(solver.Sum([y[cluster, customer] for cluster in cluster_list]) == 1)

    if enable_minimum_maximum_elements_in_a_cluster:

        logging.info('minimum number of elements in a cluster')

        # minimum number of elements in a cluster
        for cluster in cluster_list:
            solver.Add(solver.Sum([y[cluster, customer] for customer in customer_list]) >= minimum_elements_in_a_cluster)

        logging.info('maximum number of elements in a cluster')

        # maximum number of elements in a cluster
        for cluster in cluster_list:
            solver.Add(solver.Sum([y[cluster, customer] for customer in customer_list]) <= maximum_elements_in_a_cluster)
    else:

        logging.info('minimum number of elements in a cluster >= 1')

        # minimum number of elements in a cluster
        for cluster in cluster_list:
            solver.Add(solver.Sum([y[cluster, customer] for customer in customer_list]) >= 1)

    # add objective
    logging.info('Adding objective')
    solver.Minimize(solver.Sum(
        [distance[cluster, customer].WEIGHTED_DISTANCE * y[cluster, customer] for cluster, customer in
         distance.keys()]))

    # solver.Minimize(1)
    solver_parameters = pywraplp.MPSolverParameters()
    solver_parameters.SetDoubleParam(pywraplp.MPSolverParameters.RELATIVE_MIP_GAP, 0.01)
    # solver.SetTimeLimit(self.solver_time_limit)

    solver.EnableOutput()

    logging.info('Solving model')
    solution = solver.Solve()

    # get solution
    if solution == pywraplp.Solver.OPTIMAL:
        logging.info('Problem solved in {} milliseconds'.format(str(solver.WallTime())))
        logging.info('Problem solved in {} iterations'.format(str(solver.Iterations())))

        solution_final = []
        logging.info('Getting solutions')
        for cluster, customer in distance.keys():
            solution_final.append({'CLUSTER': cluster,
                                   'CUSTOMER_NAME': customer,
                                   'VALUE': y[cluster, customer].solution_value(),
                                   'DISTANCE': distance[cluster, customer].DISTANCE,
                                   'WEIGHTED_DISTANCE': distance[cluster, customer].WEIGHTED_DISTANCE})

        solution = pd.DataFrame(solution_final)

        solution = solution[solution['VALUE'] == 1]
        solution = solution[['CLUSTER', 'CUSTOMER_NAME', 'DISTANCE', 'WEIGHTED_DISTANCE']]

    else:

        solution = pd.DataFrame()

    return solution
