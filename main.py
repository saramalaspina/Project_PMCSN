from simulation.priority_scalability_simulator import better_scalability_simulation
from simulation.priority_simulator import *
from simulation.scalability_simulator import scalability_simulation
from simulation.simulator import *
import matplotlib.pyplot as plt


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
    rep_response_times = []
    seeds = []

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

    for i in range(REPLICATIONS):
        if MODEL == STANDARD:
            results, response_times = finite_simulation()
            write_file(results, file_name)
            seeds.append(results["seed"])
            append_stats(replicationStats, results)
            rep_response_times.append(response_times)
            type = "replications"
        elif MODEL == BETTER:
            results = better_finite_simulation()
            write_file(results, file_name)
            append_stats(replicationStats, results)
            type = "replications"
        elif MODEL == SCALABILITY:
            results = scalability_simulation()
            write_file1(results, file_name)
            append_scalability_stats(replicationStats, results)
            type = "scalability"
        else:
            results = better_scalability_simulation()
            write_file1(results, file_name)
            append_scalability_stats(replicationStats, results)
            type = "scalability"

    if type == "replications":
        print_simulation_stats(replicationStats, type)
    elif type == "scalability":
        print_scalability_simulation_stats(replicationStats)

    plt.figure(figsize=(10, 6))

    # Plot each run
    for run_index, response_times in enumerate(rep_response_times):
        times = [point[0] for point in response_times]
        avg_response_times = [point[1] for point in response_times]
        plt.plot(times, avg_response_times, label=f'Seed {seeds[run_index]}')

    # Aggiungi etichette, titolo, legenda e griglia
    plt.xlabel('Tempo (secondi)')
    plt.ylabel('Tempo di risposta (secondi)')
    plt.title('Analisi del transitorio')
    plt.legend()
    plt.grid(True)

    # Mostra il grafico
    plt.show()


def start_infinite_simulation():
    if MODEL == STANDARD:
        file_name = "infinite_statistics.csv"
    else:
        file_name = "better_infinite_statistics.csv"

    clear_file(file_name)

    if MODEL == STANDARD:
        batch_stats = infinite_simulation(B, K)
        print("INFINITE STANDARD SIMULATION")
    else:
        batch_stats = better_infinite_simulation(B, K)
        print("INFINITE BETTER SIMULATION")

    type = "batch"
    print_simulation_stats(batch_stats, type)

start_simulation()



