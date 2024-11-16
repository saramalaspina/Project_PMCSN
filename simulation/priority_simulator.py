from math import log
from libraries.rngs import plantSeeds, random, selectStream, getSeed  # Multi-stream generator
from simulation.simulation_output import print_all_stats
from utils.constants import*
from simulation.simulation_stats import SimulationStats
from simulation.sim_utils import*

START = 0.0  # initial time
STOP = 86400.0  # terminal (close the door) time
INFINITY = (100.0 * STOP)  # must be much larger than STOP
arrivalTemp = START  # global temp var for getArrival function

in_service = None # tracking type of job in service

plantSeeds(SEED)

# stream 0 -> arrivi dall'esterno
# stream 1 -> servizio dell'edge tipo E
# stream 2 -> servizio cloud server
# stream 3 -> probabilità di routing
# stream 4 -> servizio dell'edge tipo C

def better_finite_simulation():
    s = getSeed()
    print(s)
    reset_arrival_temp()

    stats = SimulationStats()  # init class
    stats.reset(START)  # reset stats

    # Simulation loop
    while (stats.t.arrival < STOP) or (stats.number_edge + stats.number_cloud > 0):
        stats.t.next = Min(stats.t.arrival, stats.t.completion_edge, stats.t.completion_cloud)  # next event time   */

        if (stats.number_edge > 0):  # update integrals  */
            stats.area_edge.node += (stats.t.next - stats.t.current) * stats.number_edge
            stats.area_edge.queue += (stats.t.next - stats.t.current) * (stats.number_edge - 1)
            stats.area_edge.service += (stats.t.next - stats.t.current)
        # EndIf

        if (stats.number_cloud > 0):  # update integrals  */
            stats.area_cloud.node += (stats.t.next - stats.t.current) * stats.number_cloud
            stats.area_cloud.queue += (stats.t.next - stats.t.current) * (stats.number_cloud - 1)
            stats.area_cloud.service += (stats.t.next - stats.t.current)
        # EndIf

        if (stats.number_E > 0):  # update integrals  */
            stats.area_E.node += (stats.t.next - stats.t.current) * stats.number_E
            stats.area_E.queue += (stats.t.next - stats.t.current) * (stats.number_E - 1)
            stats.area_E.service += (stats.t.next - stats.t.current)
        # EndIf

        if (stats.number_C > 0):  # update integrals  */
            stats.area_C.node += (stats.t.next - stats.t.current) * stats.number_C
            stats.area_C.queue += (stats.t.next - stats.t.current) * (stats.number_C - 1)
            stats.area_C.service += (stats.t.next - stats.t.current)
        # EndIf

        stats.t.current = stats.t.next  # advance the clock */

        if (stats.t.current == stats.t.arrival):  # process an arrival */
            stats.number_edge += 1
            stats.number_E += 1
            stats.queue_edge_E +=1
            stats.t.arrival = GetArrival()
            if (stats.t.arrival > STOP):
                stats.t.last = stats.t.current
                stats.t.arrival = INFINITY

            if (stats.number_edge == 1):
                stats.t.completion_edge = stats.t.current + GetServiceEdgeE()
                in_service = "E"
                stats.queue_edge_E -= 1

        elif stats.t.current == stats.t.completion_edge: # Process completion at edge node
            if in_service == "E":  # The job has not returned yet
                stats.number_E -=1
                stats.index_E += 1
                selectStream(3)
                if random() < P_C:  # With probability p, send job to server 2
                    stats.number_cloud += 1
                    if stats.number_cloud == 1:  # If server 2 is idle, start service
                        stats.t.completion_cloud = stats.t.current + GetServiceCloud()
                else:
                    stats.count_E += 1
            else:
                stats.count_C +=1
                stats.number_C -=1
                stats.index_C += 1

            stats.index_edge += 1
            stats.number_edge -= 1

            if stats.number_edge > 0:
                if stats.queue_edge_E:
                    stats.t.completion_edge = stats.t.current + GetServiceEdgeE()
                    in_service = "E"
                    stats.queue_edge_E -= 1
                else:
                    stats.t.completion_edge = stats.t.current + GetServiceEdgeC()
                    in_service = "C"
                    stats.queue_edge_C -= 1
            else:
                stats.t.completion_edge = INFINITY

        elif stats.t.current == stats.t.completion_cloud:  # Process completion at cloud server
            stats.index_cloud += 1
            stats.number_cloud -= 1
            if stats.number_cloud > 0:
                stats.t.completion_cloud = stats.t.current + GetServiceCloud()
            else:
                stats.t.completion_cloud = INFINITY

            stats.number_edge += 1
            stats.number_C += 1
            stats.queue_edge_C +=1
            if stats.number_edge == 1:  # If edge node is idle, start service
                stats.t.completion_edge = stats.t.current + GetServiceEdgeC()
                in_service = "C"
                stats.queue_edge_C -= 1


    # EndWhile

    # Output the statistics for edge node and cloud server
    print_all_stats(stats)

    # Collect and return the results
    return {
        'edge_avg_wait': stats.area_edge.node / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_avg_delay': stats.area_edge.queue / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_avg_service_time': stats.area_edge.service / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_utilization': stats.area_edge.service / stats.t.current if stats.t.current > 0 else 0,
        'cloud_avg_wait': stats.area_cloud.node / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_avg_delay': stats.area_cloud.queue / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_avg_service_time': stats.area_cloud.service / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_utilization': stats.area_cloud.service / stats.t.current if stats.t.current > 0 else 0,
        'count_E': stats.count_E,
        'count_C': stats.count_C
    }

better_finite_simulation()