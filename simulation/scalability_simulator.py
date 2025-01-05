from libraries.rngs import plantSeeds, getSeed
from simulation.sim_utils import*
from simulation.simulation_stats import *
from utils.constants import *
import utils.constants as cs

plantSeeds(SEED)

time_checkpoints = list(range(0, STOP, 1000))  # Checkpoint temporali ogni 1000 secondi
current_checkpoint = 0  # Indicatore del checkpoint corrente

def scalability_simulation(stop):
    global current_checkpoint
    current_checkpoint = 0

    seed = getSeed()
    set_servers(1,1)
    reset_arrival_temp()

    stats = SimulationStats()
    stats.reset(START)

    events = [event() for i in range(EDGE_SERVERS_MAX + CLOUD_SERVERS_MAX + 1)]
    # e                      # next event index                   */
    # s                      # server index                       */
    sum = [accumSum() for i in range(0, EDGE_SERVERS_MAX + CLOUD_SERVERS_MAX + 1)]

    cloud_queue = 0
    work_time = [0] * (EDGE_SERVERS_MAX + CLOUD_SERVERS_MAX)

    work_time[0] = 1 # at least one server at edge node is always allocated (100%)
    work_time[EDGE_SERVERS_MAX] = 1 # at least one server at cloud server is always allocated (100%)

    slot_time = [slotTime() for i in range(EDGE_SERVERS_MAX + CLOUD_SERVERS_MAX)]

    current_lambda = GetLambda(stats.t.current)  # update λ based on current time

    events[0].t = GetArrivalWithLambda(current_lambda)
    events[0].x = 1

    for s in range(1, EDGE_SERVERS_MAX + CLOUD_SERVERS_MAX + 1):
        events[s].t = START  # this value is arbitrary because */
        events[s].x = 0  # all servers are initially idle  */
        sum[s].service = 0.0
        sum[s].served = 0
        sum[s].servedE = 0
        sum[s].servedC = 0
        sum[s].serviceE = 0.0
        sum[s].serviceC = 0.0

    while ((events[0].x != 0) or (stats.number_edge + stats.number_cloud > 0)):
        current_lambda = GetLambda(stats.t.current)
        work_time, slot_time = AdjustServers(current_lambda, work_time, slot_time)
        e = NextEvent(events)

        stats.t.next = events[e].t # next event time  */

        if (stats.number_edge > 0):  # update integrals  */
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

        if (e == 0):  # process an arrival*/
            stats.number_edge += 1
            stats.number_E += 1
            stats.queue_edge.append("E")
            events[0].t = GetArrivalWithLambda(current_lambda)
            if (events[0].t > stop):
                events[0].x = 0
                stats.t.last = stats.t.current
            # EndIf
            if check_available_server(events, cs.EDGE_SERVERS, 1) == 1:
                s = FindOne(events, cs.EDGE_SERVERS, 1)

                if stats.queue_edge[0] == "E":
                    service = GetServiceEdgeE()
                    events[s].type = "E"
                    sum[s].serviceE += service
                    sum[s].servedE += 1
                else:
                    service = GetServiceEdgeC()
                    events[s].type = "C"
                    sum[s].serviceC += service
                    sum[s].servedC += 1

                sum[s].service += service
                sum[s].served += 1
                events[s].t = stats.t.current + service
                events[s].x = 1
                stats.queue_edge.pop(0)
            # EndIf
        # EndIf
        elif 1 <= e <= EDGE_SERVERS_MAX:  # completion at edge node
            if events[e].type == "E":
                stats.number_E -= 1
                stats.index_E += 1
                selectStream(3)
                if random() < cs.P_C:  # With probability p, send job to cloud server
                    stats.number_cloud += 1
                    cloud_queue += 1
                    if check_available_server(events, EDGE_SERVERS_MAX + cs.CLOUD_SERVERS, EDGE_SERVERS_MAX+1) == 1:
                        service = GetServiceCloud()
                        s = FindOne(events, cs.CLOUD_SERVERS + EDGE_SERVERS_MAX, EDGE_SERVERS_MAX + 1)
                        sum[s].service += service
                        sum[s].served += 1
                        events[s].t = stats.t.current + service
                        events[s].x = 1
                        events[s].type = "C"
                        cloud_queue -= 1
                else:
                    stats.count_E += 1
            else:
                stats.count_C += 1
                stats.number_C -= 1
                stats.index_C += 1

            stats.index_edge += 1
            stats.number_edge -= 1
            s = e
            if s <= cs.EDGE_SERVERS:
                if len(stats.queue_edge) != 0:
                    if stats.queue_edge[0] == "E":
                        service = GetServiceEdgeE()
                        events[s].type = "E"
                        sum[s].serviceE += service
                        sum[s].servedE += 1
                    else:
                        service = GetServiceEdgeC()
                        events[s].type = "C"
                        sum[s].serviceC += service
                        sum[s].servedC += 1
                    sum[s].service += service
                    sum[s].served += 1
                    events[s].t = stats.t.current + service
                    stats.queue_edge.pop(0)
                else:
                    events[s].x = 0
            else:
                events[s].x = 0

        elif EDGE_SERVERS_MAX + 1 <= e <= CLOUD_SERVERS_MAX + EDGE_SERVERS_MAX:  # completion at cloud server
            stats.index_cloud += 1
            stats.number_cloud -= 1

            s = e
            if s <= EDGE_SERVERS_MAX + cs.CLOUD_SERVERS:
                if cloud_queue > 0:
                    service = GetServiceCloud()
                    sum[s].service += service
                    sum[s].served += 1
                    events[s].t = stats.t.current + service
                    events[s].type = "C"
                    cloud_queue -= 1
                else:
                    events[s].x = 0
            else:
                events[s].x = 0

            stats.number_edge += 1
            stats.number_C += 1
            stats.queue_edge.append("C")

            if check_available_server(events, cs.EDGE_SERVERS, 1) == 1:
                s = FindOne(events, cs.EDGE_SERVERS, 1)

                if stats.queue_edge[0] == "E":
                    service = GetServiceEdgeE()
                    events[s].type = "E"
                    sum[s].serviceE += service
                    sum[s].servedE += 1
                else:
                    service = GetServiceEdgeC()
                    events[s].type = "C"
                    sum[s].serviceC += service
                    sum[s].servedC += 1

                sum[s].service += service
                sum[s].served += 1
                events[s].t = stats.t.current + service
                events[s].x = 1
                stats.queue_edge.pop(0)
        # EndElse
        if current_checkpoint < len(time_checkpoints) and stats.t.current >= time_checkpoints[current_checkpoint]:
            stats.edge_servers.append((stats.t.current, cs.EDGE_SERVERS))
            stats.cloud_servers.append((stats.t.current, cs.CLOUD_SERVERS))
            current_checkpoint += 1
    # EndWhile

    stats.area_edge.queue = stats.area_edge.node
    stats.area_cloud.queue = stats.area_cloud.node
    stats.area_E.queue = stats.area_E.node
    stats.area_C.queue = stats.area_C.node

    # area for each server of edge server
    for s in range(1, EDGE_SERVERS_MAX+1):
        stats.area_edge.queue -= sum[s].service
        stats.area_E.queue -= sum[s].serviceE
        stats.area_C.queue -= sum[s].serviceC

    # area for each server of cloud server
    for s in range(EDGE_SERVERS_MAX+1, CLOUD_SERVERS_MAX+EDGE_SERVERS_MAX+1):
        stats.area_cloud.queue -= sum[s].service

    # variables for multi server statistics
    edge_num_server = []
    edge_service = []
    edge_utilization = []
    edge_weight_utilization = []

    edge_serviceE = []
    edge_utilizationE = []
    edge_weight_utilizationE = []

    edge_serviceC = []
    edge_utilizationC = []
    edge_weight_utilizationC = []

    cloud_num_server = []
    cloud_service = []
    cloud_utilization = []
    cloud_weight_utilization = []

    # stats of each server at edge node for job of type E and C
    for s in range(1, EDGE_SERVERS_MAX + 1):
        edge_num_server.append(s)
        edge_utilization.append(sum[s].service / stats.t.current) if stats.t.current > 0 else 0
        edge_service.append(sum[s].service / sum[s].served) if sum[s].served > 0 else 0
        edge_utilizationE.append(sum[s].serviceE / stats.t.current) if stats.t.current > 0 else 0 # utilization of this server for job of type E
        edge_serviceE.append(sum[s].serviceE / sum[s].servedE) if sum[s].servedE > 0 else 0 # service time of this server for job of type E
        edge_utilizationC.append(sum[s].serviceC / stats.t.current) if stats.t.current > 0 else 0  # utilization of this server for job of type C
        edge_serviceC.append(sum[s].serviceC / sum[s].servedC) if sum[s].servedC > 0 else 0  # service time of this server for job of type C

    for s in range(EDGE_SERVERS_MAX +1, EDGE_SERVERS_MAX + CLOUD_SERVERS_MAX +1):
        cloud_num_server.append(s)
        cloud_service.append(sum[s].service / sum[s].served) if sum[s].served > 0 else 0
        cloud_utilization.append(sum[s].service / stats.t.current) if stats.t.current > 0 else 0

    if stats.index_C == 0:
        edge_serviceC = [0] * EDGE_SERVERS_MAX
        edge_utilizationC = [0] * EDGE_SERVERS_MAX
        cloud_service = [0] * CLOUD_SERVERS_MAX
        cloud_utilization = [0] * CLOUD_SERVERS_MAX

    for s in range(0, EDGE_SERVERS_MAX):
        edge_weight_utilization.append(edge_utilization[s] * work_time[s])
        edge_weight_utilizationE.append(edge_utilizationE[s] * work_time[s])
        edge_weight_utilizationC.append(edge_utilizationC[s] * work_time[s])

    for s in range(0, CLOUD_SERVERS_MAX):
        cloud_weight_utilization.append(cloud_utilization[s] * work_time[s])

    return {
        'stats': stats,
        'seed': seed,
        'edge_avg_wait': stats.area_edge.node / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_avg_delay': stats.area_edge.queue / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_avg_number_queue': stats.area_edge.queue / stats.t.current if stats.t.current > 0 else 0,
        'edge_server_number': edge_num_server,
        'edge_server_utilization': edge_utilization,
        'edge_weight_utilization': edge_weight_utilization,
        'edge_server_service': edge_service,
        'edge_avg_number_node': stats.area_edge.node / stats.t.current if stats.t.current > 0 else 0,

        'cloud_avg_wait': stats.area_cloud.node / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_avg_delay': stats.area_cloud.queue / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_avg_service_time': cloud_service,
        'cloud_number': cloud_num_server,
        'cloud_utilization': cloud_utilization,
        'cloud_weight_utilization': cloud_weight_utilization,
        'cloud_avg_number_node': stats.area_cloud.node / stats.t.current if stats.t.current > 0 else 0,
        'cloud_avg_number_queue': stats.area_cloud.queue / stats.t.current if stats.t.current > 0 else 0,

        'count_E': stats.count_E,
        'E_avg_wait': stats.area_E.node / stats.index_E if stats.index_E > 0 else 0,
        'E_avg_delay': stats.area_E.queue / stats.index_E if stats.index_E > 0 else 0,
        'E_avg_number_queue_edge': stats.area_E.queue / stats.t.current if stats.t.current > 0 else 0,
        'E_edge_server_utilization': edge_utilizationE,
        'edge_weight_utilizationE': edge_weight_utilizationE,
        'E_edge_server_service': edge_serviceE,
        'E_avg_number_edge': stats.area_E.node / stats.t.current if stats.t.current > 0 else 0,

        'count_C': stats.count_C,
        'C_avg_wait': stats.area_C.node / stats.index_C if stats.index_C > 0 else 0,
        'C_avg_delay': stats.area_C.queue / stats.index_C if stats.index_C > 0 else 0,
        'C_avg_number_queue_edge': stats.area_C.queue / stats.t.current if stats.t.current > 0 else 0,
        'C_edge_server_utilization': edge_utilizationC,
        'edge_weight_utilizationC': edge_weight_utilizationC,
        'C_edge_server_service': edge_serviceC,
        'C_avg_number_edge': stats.area_C.node / stats.t.current if stats.t.current > 0 else 0,
    }