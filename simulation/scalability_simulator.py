from libraries.rngs import plantSeeds, getSeed
from simulation.sim_utils import*
from simulation.simulation_stats import SimulationStats
from simulation.simulation_output import *

plantSeeds(SEED)

class event:
    t = 0  # next event time
    x = None  # event status, 0 or 1
    type = None # "E" if job E, "C" if job C in service


class time:
    current = None  # current time                       */
    next = None  # next (most imminent) event time    */


class accumSum:
    # accumulated sums of                */
    service = 0.0  # service times                    */
    serviceE = 0.0
    serviceC = 0.0
    served = 0 # number served                    */
    servedE = 0  # number type E served                    */
    servedC = 0 # number type C served                    */



def scalability_simulation():
    seed = getSeed()
    reset_arrival_temp()

    edge_server_num = 1
    cloud_server_num = 1

    stats = SimulationStats()
    stats.reset(START)

    # events = [event() for i in range(EDGE_SERVERS + CLOUD_SERVERS + 1)]
    events_edge = [event() for i in range(0, 4)]
    events_cloud = [event() for i in range(0, 3)]
    # e                      # next event index                   */
    # s                      # server index                       */
    # sum = [accumSum() for i in range(0, EDGE_SERVERS + CLOUD_SERVERS + 1)]
    sum_edge = [accumSum() for i in range(0, 4)]
    sum_cloud = [accumSum() for i in range(0, 3)]

    current_lambda = GetLambda(stats.t.current)  # update λ based on current time

    events_edge[0].t = GetArrivalWithLambda(current_lambda)
    events_edge[0].x = 1

    for s in range(1, 4):
        events_edge[s].t = START  # this value is arbitrary because */
        events_edge[s].x = 0  # all servers are initially idle  */

        sum_edge[s].service = 0.0
        sum_edge[s].served = 0
        sum_edge[s].servedE = 0
        sum_edge[s].servedC = 0
        sum_edge[s].serviceE = 0.0
        sum_edge[s].serviceC = 0.0

    for s in range(0, 3):
        events_cloud[s].t = START  # this value is arbitrary because */
        events_cloud[s].x = 0  # all servers are initially idle  */

        sum_cloud[s].service = 0.0
        sum_cloud[s].served = 0

    while (events_edge[0].x != 0) or (stats.number_edge + stats.number_cloud > 0):
        current_lambda = GetLambda(stats.t.current)  # update λ based on current time
        AdjustServers(stats, sum_edge, sum_cloud, edge_server_num, cloud_server_num)  # check utilization for authomatic scalability

        if NextEvent(events_edge, edge_server_num) < NextEvent(events_cloud, cloud_server_num): # next event index
            e = NextEvent(events_edge, edge_server_num)
            stats.t.next = events_edge[e].t  # next event time
        else:
            e = NextEvent(events_cloud,cloud_server_num)
            stats.t.next = events_cloud[e].t  # next event time

        if stats.number_edge > 0:  # update integrals  */
            stats.area_edge.node += (stats.t.next - stats.t.current) * stats.number_edge
        # EndIf

        if stats.number_cloud > 0:  # update integrals  */
            stats.area_cloud.node += (stats.t.next - stats.t.current) * stats.number_cloud
        # EndIf

        if stats.number_E > 0:  # update integrals  */
            stats.area_E.node += (stats.t.next - stats.t.current) * stats.number_E
        # EndIf

        if stats.number_C > 0:  # update integrals  */
            stats.area_C.node += (stats.t.next - stats.t.current) * stats.number_C
        # EndIf

        stats.t.current = stats.t.next  # advance the clock */

        if e == 0:  # process an arrival*/
            stats.number_edge += 1
            stats.number_E += 1
            stats.queue_edge.append("E")
            events_edge[0].t = GetArrivalWithLambda(current_lambda)
            if events_edge[0].t > STOP:
                events_edge[0].x = 0
                stats.t.last = stats.t.current
            # EndIf
            if stats.number_edge <= edge_server_num:
                s = FindOne(events_edge, edge_server_num, 1)

                if stats.queue_edge[0] == "E":
                    service = GetServiceEdgeE()
                    events_edge[s].type = "E"
                    sum_edge[s].serviceE += service
                    sum_edge[s].servedE += 1
                else:
                    service = GetServiceEdgeC()
                    events_edge[s].type = "C"
                    sum_edge[s].serviceC += service
                    sum_edge[s].servedC += 1

                sum_edge[s].service += service
                sum_edge[s].served += 1
                events_edge[s].t = stats.t.current + service
                events_edge[s].x = 1
                stats.queue_edge.pop(0)
            # EndIf
        # EndIf
        elif 0 <= e <= edge_server_num - 1:  # completion at edge node
            if events_edge[e].type == "E":
                stats.number_E -= 1
                stats.index_E += 1
                selectStream(3)
                if random() < P_C:  # With probability p, send job to cloud server
                    stats.number_cloud += 1
                    if stats.number_cloud <= cloud_server_num:
                        service = GetServiceCloud()
                        s = FindOne(events_cloud, cloud_server_num - 1, 0)
                        sum_cloud[s].service += service
                        sum_cloud[s].served += 1
                        events_cloud[s].t = stats.t.current + service
                        events_cloud[s].x = 1
                        events_cloud[s].type = "C"
                else:
                    stats.count_E += 1
            else:
                stats.count_C += 1
                stats.number_C -= 1
                stats.index_C += 1

            stats.index_edge += 1
            stats.number_edge -= 1
            s = e
            if stats.number_edge >= edge_server_num:
                if stats.queue_edge[0] == "E":
                    service = GetServiceEdgeE()
                    events_edge[s].type = "E"
                    sum_edge[s].serviceE += service
                    sum_edge[s].servedE += 1
                else:
                    service = GetServiceEdgeC()
                    events_edge[s].type = "C"
                    sum_edge[s].serviceC += service
                    sum_edge[s].servedC += 1

                sum_edge[s].service += service
                sum_edge[s].served += 1
                events_edge[s].t = stats.t.current + service
                stats.queue_edge.pop(0)
            else:
                events_edge[s].x = 0

        elif 0 <= e <= cloud_server_num - 1:  # completion at cloud server
            stats.index_cloud += 1
            stats.number_cloud -= 1

            s = e
            if stats.number_cloud >= cloud_server_num:
                service = GetServiceCloud()
                sum_cloud[s].service += service
                sum_cloud[s].served += 1
                events_cloud[s].t = stats.t.current + service
                events_cloud[s].type = "C"
            else:
                events_cloud[s].x = 0

            stats.number_edge += 1
            stats.number_C += 1
            stats.queue_edge.append("C")

            if stats.number_edge <= edge_server_num:
                s = FindOne(events_edge, edge_server_num + 1, 1)

                if stats.queue_edge[0] == "E":
                    service = GetServiceEdgeE()
                    events_edge[s].type = "E"
                    sum_edge[s].serviceE += service
                    sum_edge[s].servedE += 1
                else:
                    service = GetServiceEdgeC()
                    events_edge[s].type = "C"
                    sum_edge[s].serviceC += service
                    sum_edge[s].servedC += 1

                sum_edge[s].service += service
                sum_edge[s].served += 1
                events_edge[s].t = stats.t.current + service
                events_edge[s].x = 1
                stats.queue_edge.pop(0)
        # EndElse
    # EndWhile

    stats.area_edge.queue = stats.area_edge.node
    stats.area_cloud.queue = stats.area_cloud.node
    stats.area_E.queue = stats.area_E.node
    stats.area_C.queue = stats.area_C.node

    # area for each server of edge server
    for s in range(1, edge_server_num + 1):
        stats.area_edge.queue -= sum_edge[s].service
        stats.area_E.queue -= sum_edge[s].serviceE
        stats.area_C.queue -= sum_edge[s].serviceC

    # area for each server of cloud server
    for s in range(0, cloud_server_num):
        stats.area_cloud.queue -= sum_cloud[s].service

    # variables for multi server statistics
    edge_num_server = []
    edge_service = []
    edge_utilization = []

    edge_serviceE = []
    edge_utilizationE = []

    edge_serviceC = []
    edge_utilizationC = []

    cloud_num_server = []
    cloud_service = []
    cloud_utilization = []

    # stats of each server at edge node for job of type E and C
    for s in range(1, edge_server_num + 1):
        edge_num_server.append(s)
        edge_utilization.append(sum_edge[s].service / stats.t.current) if stats.t.current > 0 else 0
        edge_service.append(sum_edge[s].service / sum_edge[s].served) if sum_edge[s].served > 0 else 0
        edge_utilizationE.append(sum_edge[s].serviceE / stats.t.current) if stats.t.current > 0 else 0 # utilization of this server for job of type E
        edge_serviceE.append(sum_edge[s].serviceE / sum_edge[s].servedE) if sum_edge[s].servedE > 0 else 0 # service time of this server for job of type E
        edge_utilizationC.append(sum_edge[s].serviceC / stats.t.current) if stats.t.current > 0 else 0  # utilization of this server for job of type C
        edge_serviceC.append(sum_edge[s].serviceC / sum_edge[s].servedC) if sum_edge[s].servedC > 0 else 0  # service time of this server for job of type C

    for s in range(0, cloud_server_num ):
        cloud_num_server.append(s)
        cloud_service.append(sum_cloud[s].service / sum_cloud[s].served) if sum_cloud[s].served > 0 else 0
        cloud_utilization.append(sum_cloud[s].service / stats.t.current) if stats.t.current > 0 else 0

    if stats.index_C == 0:
        edge_serviceC = [0] * edge_server_num
        edge_utilizationC = [0] * edge_server_num
        cloud_service = [0] * cloud_server_num
        cloud_utilization = [0] * cloud_server_num

    return {
        'seed': seed,
        'edge_avg_wait': stats.area_edge.node / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_avg_delay': stats.area_edge.queue / stats.index_edge if stats.index_edge > 0 else 0,
        'edge_avg_number_queue': stats.area_edge.queue / stats.t.current if stats.t.current > 0 else 0,
        'edge_server_number': edge_num_server,
        'edge_server_utilization': edge_utilization,
        'edge_server_service': edge_service,
        'edge_avg_number_node': stats.area_edge.node / stats.t.current if stats.t.current > 0 else 0,

        'cloud_avg_wait': stats.area_cloud.node / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_avg_delay': stats.area_cloud.queue / stats.index_cloud if stats.index_cloud > 0 else 0,
        'cloud_avg_service_time': cloud_service,
        'cloud_number': cloud_num_server,
        'cloud_utilization': cloud_utilization,
        'cloud_avg_number_node': stats.area_cloud.node / stats.t.current if stats.t.current > 0 else 0,
        'cloud_avg_number_queue': stats.area_cloud.queue / stats.t.current if stats.t.current > 0 else 0,

        'count_E': stats.count_E,
        'E_avg_wait': stats.area_E.node / stats.index_E if stats.index_E > 0 else 0,
        'E_avg_delay': stats.area_E.queue / stats.index_E if stats.index_E > 0 else 0,
        'E_avg_number_queue_edge': stats.area_E.queue / stats.t.current if stats.t.current > 0 else 0,
        'E_edge_server_utilization': edge_utilizationE,
        'E_edge_server_service': edge_serviceE,
        'E_avg_number_edge': stats.area_E.node / stats.t.current if stats.t.current > 0 else 0,

        'count_C': stats.count_C,
        'C_avg_wait': stats.area_C.node / stats.index_C if stats.index_C > 0 else 0,
        'C_avg_delay': stats.area_C.queue / stats.index_C if stats.index_C > 0 else 0,
        'C_avg_number_queue_edge': stats.area_C.queue / stats.t.current if stats.t.current > 0 else 0,
        'C_edge_server_utilization': edge_utilizationC,
        'C_edge_server_service': edge_serviceC,
        'C_avg_number_edge': stats.area_C.node / stats.t.current if stats.t.current > 0 else 0,
    }

def GetLambda(current_time):
    # 6:00 -> 10:00 | 16:00 -> 20:00 : high time slot
    if 21600 <= current_time < 36000 or 57600 <= current_time < 72000:
        return 2.7
    # 10:00 -> 13:00 | 20:00 -> 23:00 : average time slot
    elif 36000 <= current_time < 46800 or 72000 <= current_time < 82800:
        return 1.4
    # 13:00 -> 16:00 : low time slot
    elif 46800 <= current_time < 57600:
        return 0.8
    # 23:00 -> 00:00 | 00:00 -> 6:00 -> : very low time slot
    elif 82800 <= current_time < 86400 or 0 <= current_time < 21600:
        return 0.2
    # default
    else:
        return 1.4

def AdjustServers(stats, sum_edge, sum_cloud, edge_server_num, cloud_server_num):
    edge_utilization = 0
    cloud_utilization = 0

    # calculation of the sum of server utilization in the edge node
    for s in range(1, edge_server_num + 1):
        edge_utilization += sum_edge[s].service / stats.t.current if stats.t.current > 0 else 0

    # calculation of the sum of server utilization in the cloud server
    for s in range(0, cloud_server_num):
        cloud_utilization += sum_cloud[s].service / stats.t.current if stats.t.current > 0 else 0

    # conditions for adding server
    # Edge node
    if edge_utilization / edge_server_num > 0.8:  # add 1 server for utilization > 80%
        edge_server_num += 1
        print(f"1 server added in the Edge node. Total: {edge_server_num}")

    # Cloud server
    if cloud_utilization / cloud_server_num > 0.8:  # add 1 server for utilization > 80%
        cloud_server_num += 1
        print(f"1 server added in the Cloud server. Total: {cloud_server_num}")

    # condition for removing server
    # Edge node
    if edge_server_num > 1 and edge_utilization / edge_server_num < 0.3:  # remove 1 server for utilization < 30%
        edge_server_num -= 1
        print(f"1 server removed from Edge node. Total: {edge_server_num}")

    # Cloud server
    if cloud_server_num > 1 and cloud_utilization / cloud_server_num < 0.3:  # remove 1 server for utilization < 30%
        cloud_server_num -= 1
        print(f"1 server removed from Cloud server. Total: {cloud_server_num}")

