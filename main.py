from simulation.simulator import finite_simulation
from utils.constants import *
import statistics

# Variabili per raccogliere statistiche globali
edge_wait_times = []
edge_delays = []
edge_service_times = []
edge_utilizations = []
cloud_wait_times = []
cloud_delays = []
cloud_service_times = []
cloud_utilizations = []
E_jobs_leaving = []
C_jobs_leaving = []

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

        edge_wait_times.append(results['edge_avg_wait'])
        edge_delays.append(results['edge_avg_delay'])
        edge_service_times.append(results['edge_avg_service_time'])
        edge_utilizations.append(results['edge_utilization'])
        cloud_wait_times.append(results['cloud_avg_wait'])
        cloud_delays.append(results['cloud_avg_delay'])
        cloud_service_times.append(results['cloud_avg_service_time'])
        cloud_utilizations.append(results['cloud_utilization'])
        E_jobs_leaving.append(results['count_E'])
        C_jobs_leaving.append(results['count_C'])


    # Calcolo delle medie e deviazioni standard delle replicazioni
    print(f"\nStatistiche dopo {REPLICATIONS} replicazioni:")
    print(f"Edge Node - Tempo medio di attesa: {statistics.mean(edge_wait_times):.2f} ± {statistics.stdev(edge_wait_times):.2f}")
    print(f"Edge Node - Tempo medio di ritardo: {statistics.mean(edge_delays):.2f} ± {statistics.stdev(edge_delays):.2f}")
    print(f"Edge Node - Tempo medio di servizio: {statistics.mean(edge_service_times):.2f} ± {statistics.stdev(edge_service_times):.2f}")
    print(f"Edge Node - Utilizzo: {statistics.mean(edge_utilizations):.2f} ± {statistics.stdev(edge_utilizations):.2f}")
    print(f"Cloud Server - Tempo medio di attesa: {statistics.mean(cloud_wait_times):.2f} ± {statistics.stdev(cloud_wait_times):.2f}")
    print(f"Cloud Server - Tempo medio di ritardo: {statistics.mean(cloud_delays):.2f} ± {statistics.stdev(cloud_delays):.2f}")
    print(f"Cloud Server - Tempo medio di servizio: {statistics.mean(cloud_service_times):.2f} ± {statistics.stdev(cloud_service_times):.2f}")
    print(f"Cloud Server - Utilizzo: {statistics.mean(cloud_utilizations):.2f} ± {statistics.stdev(cloud_utilizations):.2f}")
    print(f"Media E jobs leaving: {statistics.mean(E_jobs_leaving):.2f} ± {statistics.stdev(E_jobs_leaving):.2f}")
    print(f"Media C jobs leaving: {statistics.mean(C_jobs_leaving):.2f} ± {statistics.stdev(C_jobs_leaving):.2f}")

start_simulation()



