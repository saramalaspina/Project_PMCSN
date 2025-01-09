from simulation.priority_scalability_simulator import better_scalability_simulation
from simulation.priority_simulator import *
from simulation.scalability_simulator import scalability_simulation
from simulation.simulator import *


def start_simulation():
    if cs.SIMULATION_TYPE == FINITE:
        stats = start_finite_simulation()
    elif cs.SIMULATION_TYPE == INFINITE:
        stats = start_infinite_simulation()
    else:
        print("TYPE not valid!")
        exit(1)
    return stats


def start_finite_simulation():
    replicationStats = ReplicationStats()

    if cs.MODEL == STANDARD:
        file_name = "finite_statistics.csv"
        print("FINITE STANDARD SIMULATION")
    elif cs.MODEL == BETTER:
        file_name = "better_finite_statistics.csv"
        print("FINITE BETTER SIMULATION")
    elif cs.MODEL == SCALABILITY:
        file_name = "scalability_statistics.csv"
        print("FINITE SCALABILITY SIMULATION")
    else:
        file_name = "better_scalability_statistics.csv"
        print("FINITE BETTER SCALABILITY SIMULATION")

    if cs.MODEL == SCALABILITY:
        clear_scalability_file(file_name)
    else:
        clear_file(file_name)

    if cs.TRANSIENT_ANALYSIS == 1:
        stop = STOP_ANALYSIS
    else:
        stop = STOP

    for i in range(cs.REPLICATIONS):
        if cs.MODEL == STANDARD:
            results, stats = finite_simulation(stop)
            write_file(results, file_name)
            append_stats(replicationStats, results, stats)
            type = "replications"
            sim_type = "standard"
        elif cs.MODEL == BETTER:
            results, stats = better_finite_simulation(stop)
            write_file(results, file_name)
            append_stats(replicationStats, results, stats)
            type = "replications"
            sim_type = "better"
        elif cs.MODEL == SCALABILITY:
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
        plot_servers(stats, sim_type)

    if cs.TRANSIENT_ANALYSIS == 1:
        plot_analysis(replicationStats.edge_wait_interval, replicationStats.seeds, "edge_node", sim_type)
        plot_analysis(replicationStats.cloud_wait_interval, replicationStats.seeds, "cloud_server", sim_type)
        plot_analysis(replicationStats.E_wait_interval, replicationStats.seeds, "edge_node_E", sim_type)
        plot_analysis(replicationStats.C_wait_interval, replicationStats.seeds, "edge_node_C", sim_type)
    else:
        if PRINT_PLOT_TIME == 1:
            plot_wait_times(replicationStats.edge_wait_interval, sim_type, "edge_node")
            plot_wait_times(replicationStats.cloud_wait_interval, sim_type, "cloud_server")
            plot_wait_times(replicationStats.E_wait_interval, sim_type, "edge_node_E")
            plot_wait_times(replicationStats.C_wait_interval, sim_type, "edge_node_C")

    return replicationStats


def start_infinite_simulation():
    if cs.MODEL == STANDARD:
        file_name = "infinite_statistics.csv"
    else:
        file_name = "better_infinite_statistics.csv"

    clear_file(file_name)

    if cs.MODEL == STANDARD:
        batch_stats = infinite_simulation()
        print("INFINITE STANDARD SIMULATION")
    else:
        batch_stats = better_infinite_simulation()
        print("INFINITE BETTER SIMULATION")

    type = "batch"
    print_simulation_stats(batch_stats, type)
    print_autocorrelation(file_name)

    return batch_stats

def run_pc():
    if cs.MODEL == STANDARD:
        sim_type = "standard"
    elif cs.MODEL == BETTER:
        sim_type = "better"
    elif cs.MODEL == SCALABILITY:
        sim_type = "scalability"
    else:
        sim_type = "better_scalability"

    path = f"simulation/../output/plot/pc/{sim_type}/"

    if sim_type == "scalability" or sim_type == "better_scalability":
        file_name = f"finite.csv"
        plot_name = f"finite.png"
    else:
        plot_name = f"finite_{cs.LAMBDA}.png"
        file_name = f"finite_{cs.LAMBDA}.csv"

    os.makedirs(path, exist_ok=True)

    with open(f"{path}{file_name}", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Pc", "E_wait"])
        writer.writeheader()

    for i in range(0,11):
        set_probability(i/10)
        print(cs.P_C)
        stats = start_simulation()
        with open(f"{path}{file_name}", 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Pc", "E_wait"])
            data = {
                "Pc": cs.P_C,
                "E_wait": statistics.mean(stats.E_edge_wait_times)
            }
            writer.writerow(data)

    values = pd.read_csv(f"{path}{file_name}")
    p_c = values['Pc']
    E_wait = values['E_wait']

    plt.figure(figsize=(8, 5))
    plt.plot(p_c, E_wait, marker='o', linestyle='-', color='b', label='E wait time')

    plt.axhline(y=3, color='r', linestyle='--')

    plt.title('E wait times')
    plt.xlabel('Pc')
    plt.ylabel('E wait time')
    plt.grid(True)

    output_path = os.path.join(path, plot_name)
    plt.savefig(output_path)
    plt.close()

def run_lambda(lambda_values):
    if cs.MODEL == STANDARD:
        sim_type = "standard"
    else:
        sim_type = "better"

    path = f"simulation/../output/plot/lambda/{sim_type}/"

    plot_name = f"infinite.png"
    file_name = f"infinite.csv"

    os.makedirs(path, exist_ok=True)

    with open(f"{path}{file_name}", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Lambda", "E_wait"])
        writer.writeheader()

    for i in range(len(lambda_values)):
        set_lambda(lambda_values[i])
        print(cs.LAMBDA)
        stats = start_simulation()
        with open(f"{path}{file_name}", 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Lambda", "E_wait"])
            data = {
                "Lambda": cs.LAMBDA,
                "E_wait": statistics.mean(stats.E_edge_wait_times)
            }
            writer.writerow(data)

    values = pd.read_csv(f"{path}{file_name}")
    lambda_val = values['Lambda']
    E_wait = values['E_wait']

    plt.figure(figsize=(10, 6))
    plt.plot(lambda_val, E_wait, marker='o', linestyle='-', color='b', label='E wait time')

    plt.axhline(y=3, color='r', linestyle='--')

    plt.title(f'E wait times with Pc 0.4')
    plt.xlabel('Lambda')
    plt.ylabel('E wait time')
    plt.grid(True)

    output_path = os.path.join(path, plot_name)
    plt.savefig(output_path)
    plt.close()


def start():
    print("Select simulation:")
    print("1. Single simulation")
    print("2. Multiple run with different probabilities")
    print("3. Multiple run with different lambda")
    print("4. Transient analysis")
    try:
        choice = int(input("Select the number: "))
        if choice == 1:
            get_simulation()
            start_simulation()
        elif choice == 2:
            get_p_simulation()
            run_pc()
        elif choice == 3:
            get_lambda_simulation()
            lambda_values = [1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65, 1.7, 1.75]
            run_lambda(lambda_values)
        elif choice == 4:
            print("Select model:")
            print("1. Standard")
            print("2. Better")
            model = int(input("Select the number: "))
            set_transient_analysis(model)
            start_simulation()
        else:
            raise ValueError()
    except ValueError:
        print("Error: invalid choice.")

start()

