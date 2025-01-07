from libraries.rngs import * # Multi-stream generator
from utils.sim_utils import*
from utils.simulation_output import *
import utils.constants as cs
from utils.simulation_stats import*


plantSeeds(SEED)

time_checkpoints = list(range(0, STOP_ANALYSIS, 1000))  # Checkpoint temporali ogni 1000 secondi
current_checkpoint = 0  # Indicatore del checkpoint corrente

# stream 0 -> arrivi dall'esterno
# stream 1 -> servizio dell'edge tipo E
# stream 2 -> servizio cloud server
# stream 3 -> probabilità di routing
# stream 4 -> servizio dell'edge tipo C

def finite_simulation(stop):
    global  current_checkpoint
    current_checkpoint = 0
    s = getSeed()
    reset_arrival_temp()

    stats = SimulationStats()  # init class
    stats.reset(START)  # reset stats

    while (stats.t.arrival < stop) or (stats.number_edge + stats.number_cloud > 0):
        execute(stats, stop)
        if current_checkpoint < len(time_checkpoints) and stats.t.current >= time_checkpoints[current_checkpoint]:
            # Calcola il tempo di risposta medio (o altri dati rilevanti)
            edge_wait = (stats.area_edge.node / stats.index_edge) if stats.index_edge > 0 else 0
            cloud_wait = (stats.area_cloud.node / stats.index_cloud) if stats.index_cloud > 0 else 0
            E_wait = (stats.area_E.node / stats.index_E) if stats.index_E > 0 else 0
            C_wait = (stats.area_C.node / stats.index_C) if stats.index_C > 0 else 0,
            stats.edge_wait_times.append((stats.t.current, edge_wait))
            stats.cloud_wait_times.append((stats.t.current, cloud_wait))
            stats.E_wait_times.append((stats.t.current, E_wait))
            stats.C_wait_times.append((stats.t.current, C_wait))
            current_checkpoint += 1

    stats.calculate_area_queue()

    # Collect and return the results
    return return_stats(stats, stats.t.current, s), stats


def infinite_simulation():
    s = getSeed()

    start_time = 0

    batch_stats = ReplicationStats()
    stats = SimulationStats()
    stats.reset(START)  # reset stats

    while len(batch_stats.edge_wait_times) < K:

        while stats.job_arrived < B:
            execute(stats, STOP_INFINITE)
        stop_time = stats.t.current - start_time
        start_time = stats.t.current
        stats.calculate_area_queue()
        results = return_stats(stats, stop_time, s)
        write_file(results, "infinite_statistics.csv")
        append_stats(batch_stats, results, stats)
        stats.reset_infinite()

    if PRINT_PLOT_BATCH == 1:
        plot_batch(batch_stats.edge_wait_times, "standard", "edge_node")
        plot_batch(batch_stats.cloud_wait_times, "standard", "cloud_server")
        plot_batch(batch_stats.E_edge_wait_times, "standard", "edge_node_E")
        plot_batch(batch_stats.C_edge_wait_times, "standard", "edge_node_C")

    remove_batch(batch_stats, 25)
    return batch_stats

def execute(stats, stop):
    stats.t.next = Min(stats.t.arrival, stats.t.completion_edge, stats.t.completion_cloud)  # next event time   */

    if (stats.number_edge > 0): # update integrals  */
        stats.area_edge.node += (stats.t.next - stats.t.current) * stats.number_edge
    # EndIf

    if (stats.number_cloud > 0):  # update integrals  */
        stats.area_cloud.node += (stats.t.next - stats.t.current) * stats.number_cloud
    # EndIf

    if (stats.number_E > 0):  # update integrals  */
        stats.area_E.node += (stats.t.next - stats.t.current) * stats.number_E
    # EndIf

    if (stats.number_C > 0):  # update integrals  */
        stats.area_C.node += (stats.t.next - stats.t.current) * stats.number_C
    # EndIf

    stats.t.current = stats.t.next  # advance the clock */

    if (stats.t.current == stats.t.arrival):  # process an arrival */
        stats.job_arrived += 1
        stats.number_edge += 1
        stats.number_E += 1
        stats.queue_edge.append("E")
        stats.t.arrival = GetArrival()
        if (stats.t.arrival > stop):
            stats.t.last = stats.t.current
            stats.t.arrival = INFINITY

        if (stats.number_edge == 1):
            service = GetServiceEdgeE()
            stats.t.completion_edge = stats.t.current + service
            stats.area_edge.service += service
            stats.area_E.service += service

    elif stats.t.current == stats.t.completion_edge:  # Process completion at edge node
        if stats.queue_edge[0] == "E":  # The job has not returned yet
            stats.number_E -= 1
            stats.index_E += 1
            selectStream(3)
            if random() < cs.P_C:  # With probability p, send job to server 2
                stats.number_cloud += 1
                if stats.number_cloud == 1:  # If server 2 is idle, start service
                    service = GetServiceCloud()
                    stats.t.completion_cloud = stats.t.current + service
                    stats.area_cloud.service += service
            else:
                stats.count_E += 1
        else:
            stats.count_C += 1
            stats.index_C += 1
            stats.number_C -= 1

        stats.index_edge += 1
        stats.number_edge -= 1
        stats.queue_edge.pop(0)
        if stats.number_edge > 0:
            if stats.queue_edge[0] == "E":
                service = GetServiceEdgeE()
                stats.t.completion_edge = stats.t.current + service
                stats.area_edge.service += service
                stats.area_E.service += service
            else:
                service = GetServiceEdgeC()
                stats.t.completion_edge = stats.t.current + service
                stats.area_edge.service += service
                stats.area_C.service += service
        else:
            stats.t.completion_edge = INFINITY

    elif stats.t.current == stats.t.completion_cloud:  # Process completion at cloud server
        stats.index_cloud += 1
        stats.number_cloud -= 1
        if stats.number_cloud > 0:
            service = GetServiceCloud()
            stats.t.completion_cloud = stats.t.current + service
            stats.area_cloud.service += service
        else:
            stats.t.completion_cloud = INFINITY

        stats.number_edge += 1
        stats.number_C += 1
        stats.queue_edge.append("C")
        if stats.number_edge == 1:  # If edge node is idle, start service
            service = GetServiceEdgeC()
            stats.t.completion_edge = stats.t.current + service
            stats.area_edge.service += service
            stats.area_C.service += service

def return_stats(stats, t, s):
    return {
        'seed': s,
        'edge_avg_wait': stats.area_edge.node / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_avg_delay': stats.area_edge.queue / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_avg_service_time': stats.area_edge.service / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_utilization': stats.area_edge.service / t if t > 0 else 0,
        'edge_avg_number_node': stats.area_edge.node / t if t > 0 else 0,
        'edge_avg_number_queue': stats.area_edge.queue / t if t > 0 else 0,

        'cloud_avg_wait': stats.area_cloud.node / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_avg_delay': stats.area_cloud.queue / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_avg_service_time': stats.area_cloud.service / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_utilization': stats.area_cloud.service / t if t > 0 else 0,
        'cloud_avg_number_node': stats.area_cloud.node / t if t > 0 else 0,
        'cloud_avg_number_queue': stats.area_cloud.queue / t if t > 0 else 0,

        'count_E': stats.count_E,
        'E_avg_wait': stats.area_E.node / stats.index_E if stats.index_E > 0 else 0,
        'E_avg_delay': stats.area_E.queue / stats.index_E if stats.index_E > 0 else 0,
        'E_avg_service_time': stats.area_E.service / stats.index_E if stats.index_E > 0 else 0,
        'E_avg_number_edge': stats.area_E.node / t if t > 0 else 0,
        'E_avg_number_queue_edge': stats.area_E.queue / t if t > 0 else 0,
        'E_utilization': stats.area_E.service/ t if t > 0 else 0,

        'count_C': stats.count_C,
        'C_avg_wait': stats.area_C.node / stats.index_C if stats.index_C > 0 else 0,
        'C_avg_delay': stats.area_C.queue / stats.index_C if stats.index_C > 0 else 0,
        'C_avg_service_time': stats.area_C.service/ stats.index_C if stats.index_C > 0 else 0,
        'C_avg_number_edge': stats.area_C.node / t if t > 0 else 0,
        'C_avg_number_queue_edge': stats.area_C.queue / t if t > 0 else 0,
        'C_utilization': stats.area_C.service / t if t > 0 else 0
    }