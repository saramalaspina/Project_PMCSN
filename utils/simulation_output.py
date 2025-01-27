import statistics
import itertools
import csv
from utils.sim_utils import calculate_confidence_interval
import utils.constants as cs
from utils.autocorrelation import *
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils.constants import *

file_path = "simulation/../output/"

header = ["seed", "edge_avg_wait", "edge_avg_delay", "edge_avg_service_time", "edge_utilization",
              "edge_avg_number_node", "edge_avg_number_queue", "cloud_avg_wait", "cloud_avg_delay",
              "cloud_avg_service_time",
              "cloud_utilization", "cloud_avg_number_node", "cloud_avg_number_queue", "count_E", "E_avg_wait",
              "E_avg_delay", "E_avg_service_time", "E_utilization", "E_avg_number_edge", "E_avg_number_queue_edge",
              "count_C", "C_avg_wait", "C_avg_delay", "C_avg_service_time", "C_utilization", "C_avg_number_edge",
              "C_avg_number_queue_edge"]

header1 = [
    "seed", "edge_server_number", "edge_avg_wait", "edge_avg_delay", "edge_server_service",
    "edge_server_utilization", "edge_weight_utilization", "edge_avg_number_node", "edge_avg_number_queue",
    "cloud_avg_wait", "cloud_avg_delay", "cloud_avg_service_time", "cloud_utilization", "cloud_weight_utilization", "cloud_number",
    "cloud_avg_number_node", "cloud_avg_number_queue", "count_E", "E_avg_wait",
    "E_avg_delay", "E_avg_number_queue_edge", "E_edge_server_utilization", "edge_weight_utilizationE",
    "E_edge_server_service", "E_avg_number_edge", "count_C", "C_avg_wait",
    "C_avg_delay", "C_avg_number_queue_edge", "C_edge_server_utilization", "edge_weight_utilizationC",
    "C_edge_server_service", "C_avg_number_edge"
]


def print_edge_stats(stats):
    print(f"\nFor {stats.index_edge} jobs processed by edge node (first and second pass):")
    print(f"   Average wait ............ = {stats.area_edge.node / stats.index_edge:.6f}")
    print(f"   Average delay ........... = {stats.area_edge.queue / stats.index_edge:.6f}")
    print(f"   Average service time .... = {stats.area_edge.service / stats.index_edge:.6f}")
    print(f"   Average # in the node ... = {stats.area_edge.node / stats.t.current:.6f}")
    print(f"   Average # in the queue .. = {stats.area_edge.queue / stats.t.current:.6f}")
    print(f"   Utilization ............. = {stats.area_edge.service / stats.t.current:.6f}")
    print(f"   Average interarrival time = {stats.t.last / stats.index_edge:.6f}")


def print_cloud_stats(stats):
    if stats.index_cloud > 0:
        print(f"\nFor {stats.index_cloud} jobs processed by cloud server:")
        print(f"   Average wait ............ = {stats.area_cloud.node / stats.index_cloud:.6f}")
        print(f"   Average delay ........... = {stats.area_cloud.queue / stats.index_cloud:.6f}")
        print(f"   Average service time .... = {stats.area_cloud.service / stats.index_cloud:.6f}")
        print(f"   Average # in the node ... = {stats.area_cloud.node / stats.t.current:.6f}")
        print(f"   Average # in the queue .. = {stats.area_cloud.queue / stats.t.current:.6f}")
        print(f"   Utilization ............. = {stats.area_cloud.service / stats.t.current:.6f}")


def print_type_E_stats(stats):
    print(f"\nFor {stats.index_E} type E jobs processed by edge node:")
    print(f"   Average wait ............ = {stats.area_E.node / stats.index_E:.6f}")
    print(f"   Average delay ........... = {stats.area_E.queue / stats.index_E:.6f}")
    print(f"   Average service time .... = {stats.area_E.service / stats.index_E:.6f}")
    print(f"   Average # in the node ... = {stats.area_E.node / stats.t.current:.6f}")
    print(f"   Average # in the queue .. = {stats.area_E.queue / stats.t.current:.6f}")
    print(f"   Utilization ............. = {stats.area_E.service / stats.t.current:.6f}")


def print_type_C_stats(stats):
    if stats.index_C > 0:
        print(f"\nFor {stats.index_C} type C jobs in edge node:")
        print(f"   Average wait ............ = {stats.area_C.node / stats.index_C:.6f}")
        print(f"   Average delay ........... = {stats.area_C.queue / stats.index_C:.6f}")
        print(f"   Average service time .... = {stats.area_C.service / stats.index_C:.6f}")
        print(f"   Average # in the node ... = {stats.area_C.node / stats.t.current:.6f}")
        print(f"   Average # in the queue .. = {stats.area_C.queue / stats.t.current:.6f}")
        print(f"   Utilization ............. = {stats.area_C.service / stats.t.current:.6f}")


def print_job_counts(stats):
    print(f"\nNumber of type E jobs that leave the system = {stats.count_E}")
    print(f"Number of type C jobs that leave the system = {stats.count_C}")


def print_all_stats(stats):
    print_edge_stats(stats)
    print_cloud_stats(stats)
    print_type_E_stats(stats)
    print_type_C_stats(stats)
    print_job_counts(stats)


def print_scalability_simulation_stats(stats):
    print(f"\nStats after {cs.REPLICATIONS} replications:")

    # flat the list
    flat_edge_service = list(itertools.chain.from_iterable(stats.edge_service_times))
    flat_edge_utilization = [value for sublist in stats.edge_utilization for value in sublist if value != 0]

    flat_edge_serviceE = list(itertools.chain.from_iterable(stats.E_edge_service_times))
    flat_edge_utilizationE = [value for sublist in stats.E_edge_utilization for value in sublist if value != 0]

    flat_edge_serviceC = list(itertools.chain.from_iterable(stats.C_edge_service_times))
    flat_cloud_service = list(itertools.chain.from_iterable(stats.cloud_service_times))

    if (cs.P_C == 0):
        flat_cloud_utilization = [0]*CLOUD_SERVERS_MAX
        flat_edge_utilizationC = [0]*EDGE_SERVERS_MAX
    else:
        flat_edge_utilizationC = [value for sublist in stats.C_edge_utilization for value in sublist if value != 0]
        flat_cloud_utilization = [value for sublist in stats.cloud_utilization for value in sublist if value != 0]

    print(f"Edge Node - Average wait time: {statistics.mean(stats.edge_wait_times):.6f} ± {calculate_confidence_interval(stats.edge_wait_times):.6f}")
    print(f"Edge Node - Average delay time: {statistics.mean(stats.edge_delays):.6f} ± {calculate_confidence_interval(stats.edge_delays):.6f}")
    print(f"Edge Node - Average service time: {statistics.mean(flat_edge_service):.6f} ± {calculate_confidence_interval(flat_edge_service):.6f}")
    print(f"Edge Node - Utilization: {(sum(flat_edge_utilization)/cs.REPLICATIONS):.6f} ± {calculate_confidence_interval(flat_edge_utilization):.6f}")
    print(f"Edge Node - Average number in the node: {statistics.mean(stats.edge_number_node):.6f} ± {calculate_confidence_interval(stats.edge_number_node):.6f}")
    print(f"Edge Node - Average number in the queue: {statistics.mean(stats.edge_number_queue):.6f} ± {calculate_confidence_interval(stats.edge_number_queue):.6f}")

    print(f"\nCloud Server - Average wait time: {statistics.mean(stats.cloud_wait_times):.6f} ± {calculate_confidence_interval(stats.cloud_wait_times):.6f}")
    print(f"Cloud Server - Average delay time: {statistics.mean(stats.cloud_delays):.6f} ± {calculate_confidence_interval(stats.cloud_delays):.6f}")
    print(f"Cloud Server - Average service time: {statistics.mean(flat_cloud_service):.6f} ± {calculate_confidence_interval(flat_cloud_service):.6f}")
    print(f"Cloud Server - Utilization: {(sum(flat_cloud_utilization))/cs.REPLICATIONS:.6f} ± {calculate_confidence_interval(flat_cloud_utilization):.6f}")
    print(f"Cloud Server - Average number in the node: {statistics.mean(stats.cloud_number_node):.6f} ± {calculate_confidence_interval(stats.cloud_number_node):.6f}")
    print(f"Cloud Server - Average number in the queue: {statistics.mean(stats.cloud_number_queue):.6f} ± {calculate_confidence_interval(stats.cloud_number_queue):.6f}")

    print(f"\nMean E jobs leaving: {statistics.mean(stats.E_jobs_leaving):.6f} ± {calculate_confidence_interval(stats.E_jobs_leaving):.6f}")
    print(f"Average wait time for E jobs: {statistics.mean(stats.E_edge_wait_times):.6f} ± {calculate_confidence_interval(stats.E_edge_wait_times):.6f}")
    print(f"Average delay time for E jobs: {statistics.mean(stats.E_edge_delays):.6f} ± {calculate_confidence_interval(stats.E_edge_delays):.6f}")
    print(f"Average service time for E jobs: {statistics.mean(flat_edge_serviceE):.6f} ± {calculate_confidence_interval(flat_edge_serviceE):.6f}")
    print(f"Utilization for E jobs: {(sum(flat_edge_utilizationE))/cs.REPLICATIONS:.6f} ± {calculate_confidence_interval(flat_edge_utilizationE):.6f}")
    print(f"Average number of E jobs in the node (edge): {statistics.mean(stats.E_edge_number_node):.6f} ± {calculate_confidence_interval(stats.E_edge_number_node):.6f}")
    print(f"Average number of E in the (edge) queue: {statistics.mean(stats.E_edge_number_queue):.6f} ± {calculate_confidence_interval(stats.E_edge_number_queue):.6f}")

    print(f"\nMean C jobs leaving: {statistics.mean(stats.C_jobs_leaving):.6f} ± {calculate_confidence_interval(stats.C_jobs_leaving):.6f}")
    print(f"Average wait time for C jobs: {statistics.mean(stats.C_edge_wait_times):.6f} ± {calculate_confidence_interval(stats.C_edge_wait_times):.6f}")
    print(f"Average delay time for C jobs: {statistics.mean(stats.C_edge_delays):.6f} ± {calculate_confidence_interval(stats.C_edge_delays):.6f}")
    print(f"Average service time for C jobs: {statistics.mean(flat_edge_serviceC):.6f} ± {calculate_confidence_interval(flat_edge_serviceC):.6f}")
    print(f"Utilization for C jobs: {(sum(flat_edge_utilizationC))/cs.REPLICATIONS:.6f} ± {calculate_confidence_interval(flat_edge_utilizationC):.6f}")
    print(f"Average number of C jobs in the node (edge/cloud): {statistics.mean(stats.C_edge_number_node):.6f} ± {calculate_confidence_interval(stats.C_edge_number_node):.6f}")
    print(f"Average number of C in the (cloud) queue: {statistics.mean(stats.C_edge_number_queue):.6f} ± {calculate_confidence_interval(stats.C_edge_number_queue):.6f}")


def print_simulation_stats(stats, type):
    if type == "replications":
        print(f"\nStats after {cs.REPLICATIONS} replications:")
    elif type == "batch":
        print(f"\nStats for {K} batch:")

    print( f"Edge Node - Average wait time: {statistics.mean(stats.edge_wait_times):.6f} ± {calculate_confidence_interval(stats.edge_wait_times):.6f}")
    print(f"Edge Node - Average delay time: {statistics.mean(stats.edge_delays):.6f} ± {calculate_confidence_interval(stats.edge_delays):.6f}")
    print(f"Edge Node - Average service time: {statistics.mean(stats.edge_service_times):.6f} ± {calculate_confidence_interval(stats.edge_service_times):.6f}")
    print(f"Edge Node - Utilization: {statistics.mean(stats.edge_utilization):.6f} ± {calculate_confidence_interval(stats.edge_utilization):.6f}")
    print(f"Edge Node - Average number in the node: {statistics.mean(stats.edge_number_node):.6f} ± {calculate_confidence_interval(stats.edge_number_node):.6f}")
    print(f"Edge Node - Average number in the queue: {statistics.mean(stats.edge_number_queue):.6f} ± {calculate_confidence_interval(stats.edge_number_queue):.6f}")

    print(f"\nCloud Server - Average wait time: {statistics.mean(stats.cloud_wait_times):.6f} ± {calculate_confidence_interval(stats.cloud_wait_times):.6f}")
    print(f"Cloud Server - Average delay time: {statistics.mean(stats.cloud_delays):.6f} ± {calculate_confidence_interval(stats.cloud_delays):.6f}")
    print(f"Cloud Server - Average service time: {statistics.mean(stats.cloud_service_times):.6f} ± {calculate_confidence_interval(stats.cloud_service_times):.6f}")
    print(f"Cloud Server - Utilization: {statistics.mean(stats.cloud_utilization):.6f} ± {calculate_confidence_interval(stats.cloud_utilization):.6f}")
    print(f"Cloud Server - Average number in the node: {statistics.mean(stats.cloud_number_node):.6f} ± {calculate_confidence_interval(stats.cloud_number_node):.6f}")
    print(f"Cloud Server - Average number in the queue: {statistics.mean(stats.cloud_number_queue):.6f} ± {calculate_confidence_interval(stats.cloud_number_queue):.6f}")

    print(f"\nMean E jobs leaving: {statistics.mean(stats.E_jobs_leaving):.6f} ± {calculate_confidence_interval(stats.E_jobs_leaving):.6f}")
    print(f"Average wait time for E jobs: {statistics.mean(stats.E_edge_wait_times):.6f} ± {calculate_confidence_interval(stats.E_edge_wait_times):.6f}")
    print(f"Average delay time for E jobs: {statistics.mean(stats.E_edge_delays):.6f} ± {calculate_confidence_interval(stats.E_edge_delays):.6f}")
    print(f"Average service time for E jobs: {statistics.mean(stats.E_edge_service_times):.6f} ± {calculate_confidence_interval(stats.E_edge_service_times):.6f}")
    print(f"Utilization for E jobs: {statistics.mean(stats.E_edge_utilization):.6f} ± {calculate_confidence_interval(stats.E_edge_utilization):.6f}")
    print(f"Average number of E jobs in the node (edge): {statistics.mean(stats.E_edge_number_node):.6f} ± {calculate_confidence_interval(stats.E_edge_number_node):.6f}")
    print(f"Average number of E in the (edge) queue: {statistics.mean(stats.E_edge_number_queue):.6f} ± {calculate_confidence_interval(stats.E_edge_number_queue):.6f}")

    print(f"\nMean C jobs leaving: {statistics.mean(stats.C_jobs_leaving):.6f} ± {calculate_confidence_interval(stats.C_jobs_leaving):.6f}")
    print(f"Average wait time for C jobs: {statistics.mean(stats.C_edge_wait_times):.6f} ± {calculate_confidence_interval(stats.C_edge_wait_times):.6f}")
    print(f"Average delay time for C jobs: {statistics.mean(stats.C_edge_delays):.6f} ± {calculate_confidence_interval(stats.C_edge_delays):.6f}")
    print(f"Average service time for C jobs: {statistics.mean(stats.C_edge_service_times):.6f} ± {calculate_confidence_interval(stats.C_edge_service_times):.6f}")
    print(f"Utilization for C jobs: {statistics.mean(stats.C_edge_utilization):.6f} ± {calculate_confidence_interval(stats.C_edge_utilization):.6f}")
    print(f"Average number of C jobs in the node (edge/cloud): {statistics.mean(stats.C_edge_number_node):.6f} ± {calculate_confidence_interval(stats.C_edge_number_node):.6f}")
    print(f"Average number of C in the (cloud) queue: {statistics.mean(stats.C_edge_number_queue):.6f} ± {calculate_confidence_interval(stats.C_edge_number_queue):.6f}")

def print_autocorrelation(file_name):
    data = pd.read_csv(f"{file_path}{file_name}")
    columns_edge = ["edge_avg_wait", "edge_avg_delay", "edge_avg_service_time", "edge_utilization", "edge_avg_number_node", "edge_avg_number_queue"]
    columns_cloud = ["cloud_avg_wait", "cloud_avg_delay","cloud_avg_service_time","cloud_utilization", "cloud_avg_number_node", "cloud_avg_number_queue"]
    columns_E = ["E_avg_wait", "E_avg_delay", "E_avg_service_time", "E_utilization", "E_avg_number_edge","E_avg_number_queue_edge"]
    columns_C= ["C_avg_wait", "C_avg_delay", "C_avg_service_time", "C_utilization","C_avg_number_edge","C_avg_number_queue_edge"]
    print("\nAutocorrelation Edge Node")
    for col in columns_edge:
        try:
            mean, stdev, autocorr = calculate_autocorrelation(data[col].dropna().to_numpy())
            print(f"{col}: {autocorr[0]}")
        except Exception as e:
            print(f"Error {col}: {e}")

    if(cs.P_C != 0):
        print("\nAutocorrelation Cloud Server")
        for col in columns_cloud:
            try:
                mean, stdev, autocorr = calculate_autocorrelation(data[col].dropna().to_numpy())
                print(f"{col}: {autocorr[0]}")
            except Exception as e:
                print(f"Error {col}: {e}")

    print("\nAutocorrelation Edge Node type E jobs")
    for col in columns_E:
        try:
            mean, stdev, autocorr = calculate_autocorrelation(data[col].dropna().to_numpy())
            print(f"{col}: {autocorr[0]}")
        except Exception as e:
            print(f"Error {col}: {e}")

    if (cs.P_C != 0):
        print("\nAutocorrelation Edge Node type C jobs")
        for col in columns_C:
            try:
                mean, stdev, autocorr = calculate_autocorrelation(data[col].dropna().to_numpy())
                print(f"{col}: {autocorr[0]}")
            except Exception as e:
                print(f"Error {col}: {e}")


def write_file(results, file_name):
    path = file_path + file_name
    with open(path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writerow(results)

def write_file1(results, file_name):
    path = file_path + file_name
    with open(path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header1)
        writer.writerow(results)


def clear_file(file_name):
    path = file_path + file_name
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()


def clear_scalability_file(file_name):
    path = file_path + file_name
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header1)
        writer.writeheader()


def plot_analysis(wait_times, seed, name, sim_type):
    output_dir = f"simulation/../output/plot/transient_analysis/{sim_type}"

    plt.figure(figsize=(10, 6))

    # Plot each run
    for run_index, response_times in enumerate(wait_times):
        times = [point[0] for point in response_times]
        avg_response_times = [point[1] for point in response_times]
        plt.plot(times, avg_response_times, label=f'Seed {seed[run_index]}')

    plt.xlabel('Time (s)')
    plt.ylabel('Wait time (s)')
    plt.legend()
    plt.grid(True)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{name}.png')
    plt.savefig(output_path)
    plt.close()


def plot_servers(stats, sim_type):
    output_dir = f"simulation/../output/plot/servers/{sim_type}"

    plt.figure(figsize=(10, 6))

    times = [point[0] for point in stats.edge_servers]
    edge_num = [point[1] for point in stats.edge_servers]
    cloud_num = [point[1] for point in stats.cloud_servers]
    plt.plot(times, edge_num, label=f'Edge Servers', color = 'blue', linestyle='--')
    plt.plot(times, cloud_num, label=f'Cloud Servers', color = 'red', linestyle=':')

    plt.xlabel('Time (s)')
    plt.ylabel('Server')
    plt.legend()
    plt.grid(True)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{cs.P_C}.png')
    plt.savefig(output_path)
    plt.close()


def plot_wait_times(stats, sim_type, name):
    output_dir = f"simulation/../output/plot/time/{sim_type}"
    plt.figure(figsize=(10, 6))

    for run_index, response_times in enumerate(stats):
        times = [point[0] for point in response_times]
        avg_response_times = [point[1] for point in response_times]
        plt.plot(times, avg_response_times)

    plt.xlabel('Time (s)')
    plt.ylabel('Wait time (s)')
    plt.grid(True)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{name}.png')
    plt.savefig(output_path)
    plt.close()


def plot_batch(wait_times, sim_type, name):
    output_dir = f"simulation/../output/plot/batch/{sim_type}"

    x_values = [index for index in range(len(wait_times)+1)]
    y_values = [0]
    for i in range(len(wait_times)):
        y_values.append(statistics.mean(wait_times[:i+1]))

    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, linestyle='-', color='b')
    plt.xlabel('Batch')
    plt.ylabel('Wait time')
    plt.grid(True)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{name}.png')
    plt.savefig(output_path)
    plt.close()