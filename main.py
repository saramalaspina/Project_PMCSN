from simulation.priority_scalability_simulator import better_scalability_simulation
from simulation.priority_simulator import *
from simulation.scalability_simulator import scalability_simulation
from simulation.simulator import *


def start_simulation():
    if SIMULATION_TYPE == FINITE:
        start_finite_simulation()
    elif SIMULATION_TYPE == INFINITE:
        start_infinite_simulation()
    else:
        print("TYPE not valid!")
        exit(1)


def start_finite_simulation():
    replicationStats = ReplicationStats()

    if MODEL == STANDARD:
        file_name = "finite_statistics.csv"
        print("FINITE STANDARD SIMULATION")
    elif MODEL == BETTER:
        file_name = "better_finite_statistics.csv"
        print("FINITE BETTER SIMULATION")
    elif MODEL == SCALABILITY:
        file_name = "scalability_statistics.csv"
        print("FINITE SCALABILITY SIMULATION")
    else:
        file_name = "better_scalability_statistics.csv"
        print("FINITE BETTER SCALABILITY SIMULATION")

    if MODEL == SCALABILITY:
        clear_scalability_file(file_name)
    else:
        clear_file(file_name)

    if TRANSIENT_ANALYSIS == 1:
        stop = STOP_ANALYSIS
    else:
        stop = STOP

    for i in range(REPLICATIONS):
        if MODEL == STANDARD:
            results, stats = finite_simulation(stop)
            write_file(results, file_name)
            append_stats(replicationStats, results, stats)
            type = "replications"
            sim_type = "standard"
        elif MODEL == BETTER:
            results, stats = better_finite_simulation(stop)
            write_file(results, file_name)
            append_stats(replicationStats, results, stats)
            type = "replications"
            sim_type = "better"
        elif MODEL == SCALABILITY:
            results = scalability_simulation(stop)
            stats = results.pop("stats", None)
            write_file1(results, file_name)
            append_scalability_stats(replicationStats, results, stats)
            type = "scalability"
            sim_type = "scalability"
        else:
            results = better_scalability_simulation(stop)
            stats = results.pop("stats", None)
            write_file1(results, file_name)
            append_scalability_stats(replicationStats, results, stats)
            type = "scalability"
            sim_type = "better_scalability"

    if type == "replications":
        print_simulation_stats(replicationStats, type)
    elif type == "scalability":
        print_scalability_simulation_stats(replicationStats)

    plot_analysis(replicationStats.edge_wait_interval, replicationStats.seeds, "edge_node", sim_type)
    plot_analysis(replicationStats.cloud_wait_interval, replicationStats.seeds, "cloud_server", sim_type)
    plot_analysis(replicationStats.E_wait_interval, replicationStats.seeds, "edge_node_E", sim_type)
    plot_analysis(replicationStats.C_wait_interval, replicationStats.seeds, "edge_node_C", sim_type)

def start_infinite_simulation():
    if MODEL == STANDARD:
        file_name = "infinite_statistics.csv"
    else:
        file_name = "better_infinite_statistics.csv"

    clear_file(file_name)

    if MODEL == STANDARD:
        batch_stats = infinite_simulation()
        print("INFINITE STANDARD SIMULATION")
    else:
        batch_stats = better_infinite_simulation()
        print("INFINITE BETTER SIMULATION")

    type = "batch"
    print_simulation_stats(batch_stats, type)
    print_autocorrelation(file_name)

start_simulation()



