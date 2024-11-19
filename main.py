from simulation.priority_simulator import better_finite_simulation
from simulation.simulation_output import print_replication_stats, write_file, clear_file
from simulation.simulation_stats import ReplicationStats
from simulation.simulator import finite_simulation
from utils.constants import *

def start_simulation():
    if SIMULATION_TYPE == FINITE:
        start_finite_simulation()
    elif SIMULATION_TYPE == INFINITE:
        print("TODO")
    else:
        print("TYPE not valid!")
        exit(1)


def start_finite_simulation():
    replicationStats = ReplicationStats()

    if MODEL == STANDARD:
        file_name = "finite_statistics.csv"
    else:
        file_name = "better_finite_statistics.csv"

    clear_file(file_name)

    for i in range(REPLICATIONS):
        if MODEL == STANDARD:
            results = finite_simulation()
        else:
            results = better_finite_simulation()

        write_file(results, file_name)

        # append stats in the list
        replicationStats.edge_wait_times.append(results['edge_avg_wait'])
        replicationStats.edge_delays.append(results['edge_avg_delay'])
        replicationStats.edge_service_times.append(results['edge_avg_service_time'])
        replicationStats.edge_utilization.append(results['edge_utilization'])
        replicationStats.edge_number_node.append(results['edge_avg_number_node'])
        replicationStats.edge_number_queue.append(results['edge_avg_number_queue'])

        replicationStats.cloud_wait_times.append(results['cloud_avg_wait'])
        replicationStats.cloud_delays.append(results['cloud_avg_delay'])
        replicationStats.cloud_service_times.append(results['cloud_avg_service_time'])
        replicationStats.cloud_utilization.append(results['cloud_utilization'])
        replicationStats.cloud_number_node.append(results['cloud_avg_number_node'])
        replicationStats.cloud_number_queue.append(results['cloud_avg_number_queue'])

        replicationStats.E_jobs_leaving.append(results['count_E'])
        replicationStats.E_edge_wait_times.append(results['E_avg_wait'])
        replicationStats.E_edge_delays.append(results['E_avg_delay'])
        replicationStats.E_edge_service_times.append(results['E_avg_service_time'])
        replicationStats.E_edge_utilization.append(results['E_utilization'])
        replicationStats.E_edge_number_node.append(results['E_avg_number_edge'])
        replicationStats.E_edge_number_queue.append(results['E_avg_number_queue_edge'])

        replicationStats.C_jobs_leaving.append(results['count_C'])
        replicationStats.C_edge_wait_times.append(results['C_avg_wait'])
        replicationStats.C_edge_delays.append(results['C_avg_delay'])
        replicationStats.C_edge_service_times.append(results['C_avg_service_time'])
        replicationStats.C_edge_utilization.append(results['C_utilization'])
        replicationStats.C_edge_number_node.append(results['C_avg_number_edge'])
        replicationStats.C_edge_number_queue.append(results['C_avg_number_queue_edge'])

    print_replication_stats(replicationStats)

start_simulation()



