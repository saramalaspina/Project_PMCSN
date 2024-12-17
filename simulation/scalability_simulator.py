from libraries.rngs import plantSeeds, getSeed
from simulation.sim_utils import*
from simulation.simulation_stats import SimulationStats
from simulation.simulation_output import *

plantSeeds(SEED)

class event:
    t = None  # next event time
    x = None  # event status, 0 or 1
    type = None # "E" if job E, "C" if job C in service


class time:
    current = None  # current time                       */
    next = None  # next (most imminent) event time    */


class accumSum:
    # accumulated sums of                */
    service = None  # service times                    */
    serviceE = None
    serviceC = None
    served = None # number served                    */
    servedE = None  # number type E served                    */
    servedC = None # number type C served                    */

def scalability_simulation():

    area_edge = 0
    area_cloud = 0
    area_E = 0
    area_C = 0

    seed = getSeed()
    reset_arrival_temp()

    stats = SimulationStats()
    stats.reset(START)

    events = [event() for i in range(EDGE_SERVERS + CLOUD_SERVERS + 1)]
    # e                      # next event index                   */
    # s                      # server index                       */
    sum = [accumSum() for i in range(0, EDGE_SERVERS + CLOUD_SERVERS + 1)]

    events[0].t = GetArrival()
    events[0].x = 1
    for s in range(1, EDGE_SERVERS + CLOUD_SERVERS + 1):
        events[s].t = START  # this value is arbitrary because */
        events[s].x = 0  # all servers are initially idle  */
        sum[s].service = 0.0
        sum[s].served = 0
        sum[s].servedE = 0
        sum[s].servedC = 0
        sum[s].serviceE = 0.0
        sum[s].serviceC = 0.0

    while ((events[0].x != 0) or (stats.number_edge + stats.number_cloud > 0)):
        e = NextEvent(events)  # next event index */
        stats.t.next = events[e].t  # next event time  */

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

        if (e == 0):  # process an arrival*/
            stats.number_edge += 1
            stats.number_E += 1
            stats.queue_edge.append("E")
            events[0].t = GetArrival()
            if (events[0].t > STOP):
                events[0].x = 0
                stats.t.last = stats.t.current
            # EndIf
            if (stats.number_edge <= EDGE_SERVERS):
                s = FindOne(events, EDGE_SERVERS, 1)

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
        elif 1 <= e <= EDGE_SERVERS:  # completion at edge node
            if events[e].type == "E":
                stats.number_E -= 1
                stats.index_E += 1
                selectStream(3)
                if random() < P_C:  # With probability p, send job to cloud server
                    stats.number_cloud += 1
                    if stats.number_cloud <= CLOUD_SERVERS:
                        service = GetServiceCloud()
                        s = FindOne(events, CLOUD_SERVERS + EDGE_SERVERS, EDGE_SERVERS + 1)
                        sum[s].service += service
                        sum[s].serviceC += service
                        sum[s].served += 1
                        sum[s].servedC += 1
                        events[s].t = stats.t.current + service
                        events[s].x = 1
                        events[s].type = "C"
                else:
                    stats.count_E += 1
            else:
                stats.count_C += 1
                stats.number_C -= 1
                stats.index_C += 1

            stats.index_edge += 1
            stats.number_edge -= 1
            s = e
            if stats.number_edge >= EDGE_SERVERS:
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

        elif EDGE_SERVERS + 1 <= e <= CLOUD_SERVERS + EDGE_SERVERS:  # completion at cloud server
            stats.index_cloud += 1
            stats.number_cloud -= 1

            s = e
            if stats.number_cloud >= CLOUD_SERVERS:
                service = GetServiceCloud()
                sum[s].service += service
                sum[s].serviceC += service
                sum[s].served += 1
                sum[s].servedC += 1
                events[s].t = stats.t.current + service
                events[s].type = "C"
            else:
                events[s].x = 0

            stats.number_edge += 1
            stats.number_C += 1
            stats.queue_edge.append("C")

            if stats.number_edge <= EDGE_SERVERS:
                s = FindOne(events, EDGE_SERVERS, 1)

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
    # EndWhile

    area_edge = stats.area_edge.node
    area_cloud = stats.area_cloud.node
    area_E = stats.area_E.node
    area_C = stats.area_C.node

    # area for each server of edge server
    for s in range(1, EDGE_SERVERS+1):
        area_edge -= sum[s].service
        area_E -= sum[s].serviceE
        area_C -= sum[s].serviceC

    # area for each server of cloud server
    for s in range(EDGE_SERVERS+1, CLOUD_SERVERS+EDGE_SERVERS+1):
        area_cloud -= sum[s].service

    # variables for multi server statistics
    edge_num_server = []
    edge_server_service = []
    edge_server_utilization = []

    edge_server_serviceE = []
    edge_server_utilizationE = []

    edge_server_serviceC = []
    edge_server_utilizationC = []

    # for cloud server we assume that it remain a single server

    # stats of each server at edge node for job of type E and C
    for s in range(1, EDGE_SERVERS + 1):
        edge_num_server.append(s)
        edge_server_utilization.append(sum[s].service / stats.t.current) if stats.t.current > 0 else 0
        edge_server_service.append(sum[s].service / sum[s].served) if sum[s].served > 0 else 0

    # stats of each server at edge node for job of type E and type C
    for s in range(1, EDGE_SERVERS + 1):
        edge_server_utilizationE.append(sum[s].serviceE / stats.t.current) if stats.t.current > 0 else 0 # utilization of this server for job of type E
        edge_server_serviceE.append(sum[s].serviceE / sum[s].servedE) if sum[s].servedE > 0 else 0 # service time of this server for job of type E

        edge_server_utilizationC.append(sum[s].serviceC / stats.t.current) if stats.t.current > 0 else 0  # utilization of this server for job of type C
        edge_server_serviceC.append(sum[s].serviceC / sum[s].servedC) if sum[s].servedC > 0 else 0  # service time of this server for job of type C

    # stats of each server at cloud server (type C job)
    # for s in range(EDGE_SERVERS + 1, CLOUD_SERVERS + EDGE_SERVERS + 1):
        # edge_server_utilizationC.append(sum[s].serviceC / stats.t.current) if stats.t.current > 0 else 0 # utilization of this server for job of type C
        # edge_server_serviceC.append(sum[s].serviceC / sum[s].servedC) if sum[s].servedC > 0 else 0 # service time of this server for job of type C

    if(stats.index_C == 0):
        edge_server_serviceC = [0] * EDGE_SERVERS
        edge_server_utilizationC = [0] * EDGE_SERVERS

    return {
        'seed': seed,
        'edge_avg_wait': stats.area_edge.node / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_avg_delay': area_edge / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_avg_number_queue': area_edge / stats.t.current if stats.t.current > 0 else 0,
        'server_number': edge_num_server,
        'edge_server_utilization': edge_server_utilization,
        'edge_server_service': edge_server_service,
        'edge_avg_number_node': stats.area_edge.node / stats.t.current if stats.t.current > 0 else 0,

        'cloud_avg_wait': stats.area_cloud.node / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_avg_delay': stats.area_cloud.queue / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_avg_service_time': stats.area_cloud.service / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_utilization': stats.area_cloud.service / stats.t.current if stats.t.current > 0 else 0,
        'cloud_avg_number_node': stats.area_cloud.node / stats.t.current if stats.t.current > 0 else 0,
        'cloud_avg_number_queue': stats.area_cloud.queue / stats.t.current if stats.t.current > 0 else 0,

        'count_E': stats.count_E,
        'E_avg_wait': stats.area_E.node / stats.index_E if stats.index_E > 0 else 0,
        'E_avg_delay': area_E / stats.index_E if stats.index_E > 0 else 0,
        'E_avg_number_queue_edge': area_E / stats.t.current if stats.t.current > 0 else 0,
        'E_edge_server_utilization': edge_server_utilizationE,
        'E_edge_server_service': edge_server_serviceE,
        'E_avg_number_edge': stats.area_E.node / stats.t.current if stats.t.current > 0 else 0,

        'count_C': stats.count_C,
        'C_avg_wait': stats.area_C.node / stats.index_C if stats.index_C > 0 else 0,
        'C_avg_delay': area_C / stats.index_C if stats.index_C > 0 else 0,
        'C_avg_number_queue_edge': area_C / stats.t.current if stats.t.current > 0 else 0,
        'C_edge_server_utilization': edge_server_utilizationC,
        'C_edge_server_service': edge_server_serviceC,
        'C_avg_number_edge': stats.area_C.node / stats.t.current if stats.t.current > 0 else 0,
    }

