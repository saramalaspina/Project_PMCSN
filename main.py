from simulation.sim_utils import calculate_confidence_interval
from simulation.simulator import finite_simulation
from utils.constants import *
import statistics

# lists for edge stats
edge_wait_times = []
edge_delays = []
edge_service_times = []
edge_utilization = []
edge_number_node = []
edge_number_queue = []

# lists for cloud stats
cloud_wait_times = []
cloud_delays = []
cloud_service_times = []
cloud_utilization = []
cloud_number_node = []
cloud_number_queue = []

# lists for E type job stats
E_jobs_leaving = []
E_edge_wait_times = []
E_edge_delays = []
E_edge_service_times = []
E_edge_utilization = []
E_edge_number_node = []
E_edge_number_queue = []

# lists for C type job stats
C_jobs_leaving = []
C_edge_wait_times = []
C_edge_delays = []
C_edge_service_times = []
C_edge_utilization = []
C_edge_number_node = []
C_edge_number_queue = []

def start_simulation():
    if SIMULATION_TYPE == FINITE:
        start_finite_simulation()
    elif SIMULATION_TYPE == INFINITE:
        print("TODO")
    else:
        print("TYPE not valid!")
        exit(1)


def start_finite_simulation():
    for i in range(REPLICATIONS):
        results = finite_simulation()

        # append stats in the list
        edge_wait_times.append(results['edge_avg_wait'])
        edge_delays.append(results['edge_avg_delay'])
        edge_service_times.append(results['edge_avg_service_time'])
        edge_utilization.append(results['edge_utilization'])
        edge_number_node.append(results['edge_avg_number_node'])
        edge_number_queue.append(results['edge_avg_number_queue'])

        cloud_wait_times.append(results['cloud_avg_wait'])
        cloud_delays.append(results['cloud_avg_delay'])
        cloud_service_times.append(results['cloud_avg_service_time'])
        cloud_utilization.append(results['cloud_utilization'])
        cloud_number_node.append(results['cloud_avg_number_node'])
        cloud_number_queue.append(results['cloud_avg_number_queue'])

        E_jobs_leaving.append(results['count_E'])
        E_edge_wait_times.append(results['E_avg_wait'])
        E_edge_delays.append(results['E_avg_delays'])
        E_edge_service_times.append(results['E_avg_service_time'])
        E_edge_utilization.append(results['E_utilization'])
        E_edge_number_node.append(results['E_avg_number_node'])
        E_edge_number_queue.append(results['E_avg_number_queue'])

        C_jobs_leaving.append(results['count_C'])
        C_edge_wait_times.append(results['C_avg_wait'])
        C_edge_delays.append(results['C_avg_delays'])
        C_edge_service_times.append(results['C_avg_service_time'])
        C_edge_utilization.append(results['C_utilization'])
        C_edge_number_node.append(results['C_avg_number_node'])
        C_edge_number_queue.append(results['C_avg_number_queue'])

    # get mean and standard deviation
    print(f"\nStats after {REPLICATIONS} replications:")
    print(f"Edge Node - Average wait time: {statistics.mean(edge_wait_times):.2f} ± {calculate_confidence_interval(edge_wait_times):.2f}")
    print(f"Edge Node - Average delay time: {statistics.mean(edge_delays):.2f} ± {calculate_confidence_interval(edge_delays):.2f}")
    print(f"Edge Node - Average service time: {statistics.mean(edge_service_times):.2f} ± {calculate_confidence_interval(edge_service_times):.2f}")
    print(f"Edge Node - Utilization: {statistics.mean(edge_utilization):.2f} ± {calculate_confidence_interval(edge_utilization):.2f}")
    print(f"Edge Node - Average number in the node: {statistics.mean(edge_number_node):.2f} ± {calculate_confidence_interval(edge_number_node):.2f}")
    print(f"Edge Node - Average number in the queue: {statistics.mean(edge_number_queue):.2f} ± {calculate_confidence_interval(edge_number_queue):.2f}")

    print(f"Cloud Server - Average wait time: {statistics.mean(cloud_wait_times):.2f} ± {calculate_confidence_interval(cloud_wait_times):.2f}")
    print(f"Cloud Server - Average delay time: {statistics.mean(cloud_delays):.2f} ± {calculate_confidence_interval(cloud_delays):.2f}")
    print(f"Cloud Server - Average service time: {statistics.mean(cloud_service_times):.2f} ± {calculate_confidence_interval(cloud_service_times):.2f}")
    print(f"Cloud Server - Utilization: {statistics.mean(cloud_utilization):.2f} ± {calculate_confidence_interval(cloud_utilization):.2f}")
    print(f"Cloud Node - Average number in the node: {statistics.mean(cloud_number_node):.2f} ± {calculate_confidence_interval(cloud_number_node):.2f}")
    print(f"Cloud Node - Average number in the queue: {statistics.mean(cloud_number_queue):.2f} ± {calculate_confidence_interval(cloud_number_queue):.2f}")

    print(f"Mean E jobs leaving: {statistics.mean(E_jobs_leaving):.2f} ± {calculate_confidence_interval(E_jobs_leaving):.2f}")
    print(f"Average wait time for E jobs: {statistics.mean(E_edge_wait_times):.2f} ± {calculate_confidence_interval(E_edge_wait_times):.2f}")
    print(f"Average delay time for E jobs: {statistics.mean(E_edge_delays):.2f} ± {calculate_confidence_interval(E_edge_delays):.2f}")
    print(f"Average service time for E jobs: {statistics.mean(E_edge_service_times):.2f} ± {calculate_confidence_interval(E_edge_service_times):.2f}")
    print(f"Utilization for E jobs: {statistics.mean(E_edge_utilization):.2f} ± {calculate_confidence_interval(E_edge_utilization):.2f}")
    print(f"Average number of E jobs in the node (edge): {statistics.mean(E_edge_number_node):.2f} ± {calculate_confidence_interval(E_edge_number_node):.2f}")
    print(f"Average number of E in the (edge) queue: {statistics.mean(E_edge_number_queue):.2f} ± {calculate_confidence_interval(E_edge_number_queue):.2f}")

    print(f"Mean C jobs leaving: {statistics.mean(C_jobs_leaving):.2f} ± {calculate_confidence_interval(C_jobs_leaving):.2f}")
    print(f"Average wait time for C jobs: {statistics.mean(C_edge_wait_times):.2f} ± {calculate_confidence_interval(C_edge_wait_times):.2f}")
    print(f"Average delay time for C jobs: {statistics.mean(C_edge_delays):.2f} ± {calculate_confidence_interval(C_edge_delays):.2f}")
    print(f"Average service time for C jobs: {statistics.mean(C_edge_service_times):.2f} ± {calculate_confidence_interval(C_edge_service_times):.2f}")
    print(f"Utilization for C jobs: {statistics.mean(C_edge_utilization):.2f} ± {calculate_confidence_interval(C_edge_utilization):.2f}")
    print(f"Average number of C jobs in the node (edge/cloud): {statistics.mean(C_edge_number_node):.2f} ± {calculate_confidence_interval(C_edge_number_node):.2f}")
    print(f"Average number of C in the (cloud) queue: {statistics.mean(C_edge_number_queue):.2f} ± {calculate_confidence_interval(C_edge_number_queue):.2f}")


start_simulation()



