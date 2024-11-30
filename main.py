from simulation.priority_scalability_simulator import better_scalability_simulation
from simulation.priority_simulator import *
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
    else:
        file_name = "better_scalability_statistics.csv"
        print("FINITE BETTER SCALABILITY SIMULATION")


    clear_file(file_name)

    for i in range(REPLICATIONS):
        if MODEL == STANDARD:
            results = finite_simulation()
        elif MODEL == BETTER:
            results = better_finite_simulation()
        else:
            results = better_scalability_simulation()

        write_file(results, file_name)

        append_stats(replicationStats, results)

    type = "replications"
    print_simulation_stats(replicationStats, type)

def start_infinite_simulation():
    if MODEL == STANDARD:
        file_name = "infinite_statistics.csv"
    else:
        file_name = "better_infinite_statistics.csv"

    clear_file(file_name)

    if MODEL == STANDARD:
        batch_stats = infinite_simulation(B, K)
        print("FINITE STANDARD SIMULATION")
    else:
        batch_stats = better_infinite_simulation(B, K)
        print("FINITE BETTER SIMULATION")

    type = "batch"
    print_simulation_stats(batch_stats, type)

start_simulation()



