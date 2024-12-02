import math
from math import log
from libraries import rngs, rvms
from libraries.rngs import selectStream, random
from utils.constants import *
import statistics

arrivalTemp = START

streams = {
    'edge_node': 1,
    'cloud_server': 2
}

service_rates = {
    'edge_node': 0.5,
    'cloud_server': 0.8
}

def get_next_arrival_time(mean_arrival_time):
    rngs.selectStream(0)
    return rvms.idfExponential(mean_arrival_time, rngs.random())

def get_service_time(stream):
    rngs.selectStream(streams[stream])
    service_time = rvms.idfExponential(service_rates[stream], rngs.random())
    return service_time

def Min(a, b, c):
    """Return the smallest of a, b, c."""
    return min(a, b, c)


def Exponential(m):
    """Generate an Exponential random variate, use m > 0.0."""
    return (-m * log(1.0 - random()))


def Uniform(a, b):
    """Generate a Uniform random variate, use a < b."""
    return (a + (b - a) * random())


def GetArrival():
    """Generate the next arrival time for the first server."""
    global arrivalTemp
    selectStream(0)
    arrivalTemp += Exponential(1 / MEAN_ARRIVAL_TIME)
    return arrivalTemp

def reset_arrival_temp():
    global arrivalTemp
    arrivalTemp = START


def GetServiceEdgeE():
    """Generate the next service time for both servers."""
    selectStream(1)
    return Exponential(0.5)

def GetServiceEdgeC():
    """Generate the second service time at the edge after returning from the cloud."""
    selectStream(4)
    return Exponential(0.1)

def GetServiceCloud():
    """Generate the next service time for both servers."""
    selectStream(2)
    return Exponential(0.8)

def calculate_confidence_interval(data):
    n = len(data)
    if n == 0:
        return 0.0, 0.0  # no data

    standard_deviation = statistics.stdev(data)

    # get t* for interval confidence
    t_star = rvms.idfStudent(n - 1, 1 - ALPHA / 2)

    # calculate confidence interval
    margin_of_error = t_star * standard_deviation / math.sqrt(n - 1)

    return margin_of_error

def NextEvent(events):
    i = 0
    while events[i].x == 0:  # find the index of the first 'active' */
        i += 1  # element in the event list            */
    # EndWhile
    e = i
    while i < EDGE_SERVERS + CLOUD_SERVERS:  # now, check the others to find which  */
        i += 1  # event type is most imminent          */
        if (events[i].x == 1) and (events[i].t < events[e].t):
            e = i
    # EndWhile
    return (e)


def FindOne(events, servers, i):
    while events[i].x == 1:  # find the index of the first available */
        i += 1  # (idle) server
    # EndWhile
    s = i
    while i < servers:  # now, check the others to find which   */
        i += 1  # has been idle longest                 */
        if (events[i].x == 0) and (events[i].t < events[s].t):
            s = i
    # EndWhile
    return (s)

def append_stats(replicationStats, results):
    # append stats in the list
    replicationStats.edge_wait_times.append(results['edge_avg_wait'])
    replicationStats.edge_delays.append(results['edge_avg_delay'])
    replicationStats.edge_service_times.append(results['edge_avg_service_time'])
    replicationStats.edge_utilization.append(results['edge_utilization'])
    replicationStats.edge_number_node.append(results['edge_avg_number_node'])
    replicationStats.edge_number_queue.append(results['edge_avg_number_queue'])

    replicationStats.cloud_wait_times.append(results['cloud_avg_wait'])
    replicationStats.cloud_delays.append(results['cloud_avg_delay'])
    replicationStats.cloud_service_times.append(results['cloud_avg_service_time'])
    replicationStats.cloud_utilization.append(results['cloud_utilization'])
    replicationStats.cloud_number_node.append(results['cloud_avg_number_node'])
    replicationStats.cloud_number_queue.append(results['cloud_avg_number_queue'])

    replicationStats.E_jobs_leaving.append(results['count_E'])
    replicationStats.E_edge_wait_times.append(results['E_avg_wait'])
    replicationStats.E_edge_delays.append(results['E_avg_delay'])
    replicationStats.E_edge_service_times.append(results['E_avg_service_time'])
    replicationStats.E_edge_utilization.append(results['E_utilization'])
    replicationStats.E_edge_number_node.append(results['E_avg_number_edge'])
    replicationStats.E_edge_number_queue.append(results['E_avg_number_queue_edge'])

    replicationStats.C_jobs_leaving.append(results['count_C'])
    replicationStats.C_edge_wait_times.append(results['C_avg_wait'])
    replicationStats.C_edge_delays.append(results['C_avg_delay'])
    replicationStats.C_edge_service_times.append(results['C_avg_service_time'])
    replicationStats.C_edge_utilization.append(results['C_utilization'])
    replicationStats.C_edge_number_node.append(results['C_avg_number_edge'])
    replicationStats.C_edge_number_queue.append(results['C_avg_number_queue_edge'])




