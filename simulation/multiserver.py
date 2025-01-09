import csv
import os
import statistics

import numpy as np

from libraries.rngs import plantSeeds, getSeed
from utils.sim_utils import*
from utils.simulation_stats import *
from utils.constants import *
import utils.constants as cs

plantSeeds(SEED)

def multiserver_simultation(current_lambda):
    reset_arrival_temp()

    stats = SimulationStats()
    stats.reset(START)

    events = [event() for i in range(EDGE_SERVERS + CLOUD_SERVERS + 1)]
    # e                      # next event index                   */
    # s                      # server index                       */
    sum = [accumSum() for i in range(0, EDGE_SERVERS + CLOUD_SERVERS + 1)]

    cloud_queue = 0

    events[0].t = GetArrivalWithLambda(current_lambda)
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
            if (events[0].t > STOP):
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
        elif 1 <= e <= EDGE_SERVERS:  # completion at edge node
            if events[e].type == "E":
                stats.number_E -= 1
                stats.index_E += 1
                selectStream(3)
                if random() < cs.P_C:  # With probability p, send job to cloud server
                    stats.number_cloud += 1
                    cloud_queue += 1
                    if check_available_server(events, EDGE_SERVERS + cs.CLOUD_SERVERS, EDGE_SERVERS+1) == 1:
                        service = GetServiceCloud()
                        s = FindOne(events, cs.CLOUD_SERVERS + EDGE_SERVERS, EDGE_SERVERS + 1)
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

        elif EDGE_SERVERS + 1 <= e <= CLOUD_SERVERS + EDGE_SERVERS:  # completion at cloud server
            stats.index_cloud += 1
            stats.number_cloud -= 1

            s = e
            if s <= EDGE_SERVERS + cs.CLOUD_SERVERS:
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
    # EndWhile

    wait_E = stats.area_E.node / stats.index_E if stats.index_E > 0 else 0

    return wait_E

def start_multiserver():
    #lambda_values = [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
    #lambda_values = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6]
    #lambda_values = [0.4, 1.0, 1.6, 2.2, 2.8, 3.4, 4.0, 4.6, 5.2]
    lambda_values = [3.4]
    replication_res = []
    lambda_res = []
    for i in range(len(lambda_values)):
        for j in range(10):
            wait_time = multiserver_simultation(lambda_values[i])
            replication_res.append(wait_time)

        avg_wait = statistics.mean(replication_res)
        print(f"Wait time E {avg_wait}, for lambda {lambda_values[i]}")
        lambda_res.append((lambda_values[i],avg_wait))
        replication_res = []

    file_exists = os.path.isfile("multiserver.csv")

    with open("multiserver.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Lambda", "E wait time", "Edge Servers"])

        for first, second in lambda_res:
            writer.writerow([first, second, EDGE_SERVERS])

start_multiserver()




