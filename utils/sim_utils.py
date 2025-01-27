import math
from math import log
from libraries import rvms
from libraries.rngs import selectStream, random
import statistics
import utils.constants as cs

arrivalTemp = cs.START

streams = {
    'edge_node': 1,
    'cloud_server': 2
}

service_rates = {
    'edge_node': 0.5,
    'cloud_server': 0.8
}


def Min(a, b, c):
    """Return the smallest of a, b, c."""
    return min(a, b, c)


def Exponential(m):
    """Generate an Exponential random variate, use m > 0.0."""
    return -m * log(1.0 - random())


def Uniform(a, b):
    """Generate a Uniform random variate, use a < b."""
    return a + (b - a) * random()


def idfTruncatedNormal(m, s, a, b):
    alpha = rvms.cdfNormal(m, s, a)          # a = 0
    beta = 1.0 - rvms.cdfNormal(m, s, b)     # b = 2
    u = rvms.idfUniform(alpha, 1.0 - beta, random())
    return rvms.idfNormal(m, s, u)


def GetArrival():
    """Generate the next arrival time for the first server."""
    global arrivalTemp
    selectStream(0)
    arrivalTemp += Exponential(1 / cs.LAMBDA)
    return arrivalTemp


def GetArrivalWithLambda(current_lambda):
    """Generate the next arrival time with a dynamic lambda."""
    global arrivalTemp
    selectStream(0)
    arrivalTemp += Exponential(1 / current_lambda)
    return arrivalTemp


def reset_arrival_temp():
    global arrivalTemp
    arrivalTemp = cs.START


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

    if n > 1:
        standard_deviation = statistics.stdev(data)
    else:
        standard_deviation = 0
        return standard_deviation

    # get t* for interval confidence
    t_star = rvms.idfStudent(n - 1, 1 - cs.ALPHA / 2)

    # calculate confidence interval
    margin_of_error = t_star * standard_deviation / math.sqrt(n - 1)

    return margin_of_error


def NextEvent(events):
    i = 0
    while events[i].x == 0:  # find the index of the first 'active' */
        i += 1  # element in the event list            */
    # EndWhile
    e = i
    while i < cs.EDGE_SERVERS_MAX + cs.CLOUD_SERVERS_MAX:  # now, check the others to find which  */
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


def append_stats(replicationStats, results, stats):
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

    replicationStats.edge_wait_interval.append(stats.edge_wait_times)
    replicationStats.cloud_wait_interval.append(stats.cloud_wait_times)
    replicationStats.E_wait_interval.append(stats.E_wait_times)
    replicationStats.C_wait_interval.append(stats.C_wait_times)

    replicationStats.seeds.append(results['seed'])

def append_scalability_stats(replicationStats, results, stats):
    # append stats in the list
    replicationStats.edge_wait_times.append(results['edge_avg_wait'])
    replicationStats.edge_delays.append(results['edge_avg_delay'])
    replicationStats.edge_service_times.append(results['edge_server_service'])
    replicationStats.edge_utilization.append(results['edge_weight_utilization'])
    replicationStats.edge_number_node.append(results['edge_avg_number_node'])
    replicationStats.edge_number_queue.append(results['edge_avg_number_queue'])

    replicationStats.cloud_wait_times.append(results['cloud_avg_wait'])
    replicationStats.cloud_delays.append(results['cloud_avg_delay'])
    replicationStats.cloud_service_times.append(results['cloud_avg_service_time'])
    replicationStats.cloud_utilization.append(results['cloud_weight_utilization'])
    replicationStats.cloud_number_node.append(results['cloud_avg_number_node'])
    replicationStats.cloud_number_queue.append(results['cloud_avg_number_queue'])

    replicationStats.E_jobs_leaving.append(results['count_E'])
    replicationStats.E_edge_wait_times.append(results['E_avg_wait'])
    replicationStats.E_edge_delays.append(results['E_avg_delay'])
    replicationStats.E_edge_service_times.append(results['E_edge_server_service'])
    replicationStats.E_edge_utilization.append(results['edge_weight_utilizationE'])
    replicationStats.E_edge_number_node.append(results['E_avg_number_edge'])
    replicationStats.E_edge_number_queue.append(results['E_avg_number_queue_edge'])

    replicationStats.C_jobs_leaving.append(results['count_C'])
    replicationStats.C_edge_wait_times.append(results['C_avg_wait'])
    replicationStats.C_edge_delays.append(results['C_avg_delay'])
    replicationStats.C_edge_service_times.append(results['C_edge_server_service'])
    replicationStats.C_edge_utilization.append(results['edge_weight_utilizationC'])
    replicationStats.C_edge_number_node.append(results['C_avg_number_edge'])
    replicationStats.C_edge_number_queue.append(results['C_avg_number_queue_edge'])

    replicationStats.edge_wait_interval.append(stats.edge_wait_times)
    replicationStats.cloud_wait_interval.append(stats.cloud_wait_times)
    replicationStats.E_wait_interval.append(stats.E_wait_times)
    replicationStats.C_wait_interval.append(stats.C_wait_times)

    replicationStats.seeds.append(results['seed'])

def check_available_server(events, servers, i):
    found = 0
    while i <= servers and found == 0:
        if events[i].x == 0:
            found = 1
        i += 1
    return found


def GetLambda(current_time):
    # 6:00 -> 10:00 | 16:00 -> 20:00 : high time slot
    if 21600 <= current_time < 36000 or 57600 <= current_time < 72000:
        return 2.5
    # 10:00 -> 13:00 | 20:00 -> 23:00 : average time slot
    elif 36000 <= current_time < 46800 or 72000 <= current_time < 82800:
        return 1.4
    # 13:00 -> 16:00 : low time slot
    elif 46800 <= current_time < 57600:
        return 0.8
    # 23:00 -> 00:00 | 00:00 -> 6:00 -> : very low time slot
    elif 82800 <= current_time < 86400 or 0 <= current_time < 21600:
        return 0.4
    # default
    else:
        return 1.4


def AdjustServers(current_lambda, work_time, slot_time):
    edge_utilization = current_lambda * (0.5+0.1*cs.P_C)
    cloud_utilization = (current_lambda * cs.P_C) * 0.8

    # conditions for adding server
    # Edge node
    if cs.EDGE_SERVERS < cs.EDGE_SERVERS_MAX and edge_utilization / cs.EDGE_SERVERS > 0.8:  # add 1 server for utilization > 80%
        cs.increment_edge()
        work_time, slot_time = set_work_time(current_lambda, work_time, slot_time, cs.EDGE_SERVERS)

    # Cloud server
    if cs.CLOUD_SERVERS < cs.CLOUD_SERVERS_MAX and cloud_utilization / cs.CLOUD_SERVERS > 0.8:  # add 1 server for utilization > 80%
        cs.increment_cloud()
        work_time, slot_time = set_work_time(current_lambda, work_time, slot_time, cs.EDGE_SERVERS_MAX + cs.CLOUD_SERVERS)

    # condition for removing server
    # Edge node
    if cs.EDGE_SERVERS > 1 and edge_utilization / cs.EDGE_SERVERS < 0.3:  # remove 1 server for utilization < 30%
        cs.decrement_edge()

    # Cloud server
    if cs.CLOUD_SERVERS > 1 and cloud_utilization / cs.CLOUD_SERVERS < 0.3:  # remove 1 server for utilization < 30%
        cs.decrement_cloud()

    return work_time, slot_time


def set_work_time (current_lambda, work_time, slot_time, num_server):
    # this function calculates the fraction of work of a server based on slot time
    if current_lambda == 2.5 and slot_time[num_server - 1].highSlotTime == 0:
        slot_time[num_server - 1].highSlotTime = 1
        work_time[num_server - 1] += 8/24
    elif current_lambda == 1.4 and slot_time[num_server - 1].averageSlotTime == 0:
        slot_time[num_server - 1].averageSlotTime = 1
        work_time[num_server - 1] += 6/24
    elif current_lambda == 0.8 and slot_time[num_server - 1].lowSlotTime == 0:
        slot_time[num_server - 1].lowSlotTime = 1
        work_time[num_server - 1] += 3/24
    elif current_lambda == 0.4 and slot_time[num_server - 1].minSlotTime == 0:
        slot_time[num_server - 1].minSlotTime = 1
        work_time[num_server - 1] += 7/24

    return work_time, slot_time

def remove_batch(stats, n):
    if n < 0:
        raise ValueError()
    for attr in dir(stats):
        value = getattr(stats, attr)
        if isinstance(value, list):
            setattr(stats, attr, value[n:])


def get_simulation():
    print("Select model:")
    print("1. Standard")
    print("2. Better")
    print("3. Standard Scalability")
    print("4. Better Scalability")
    model = int(input("Select the number: "))

    if model < 1 or model > 4:
        raise ValueError()

    if model == 3 or model == 4:
        sim = 1
    else:
        print("Select simulation:")
        print("1. Finite")
        print("2. Infinite")
        sim = int(input("Select the number: "))

    if sim < 1 or sim > 2:
        raise ValueError()

    cs.set_simulation(model, sim)


def get_lambda_simulation():
    print("Select model:")
    print("1. Standard")
    print("2. Better")
    model = int(input("Select the number: "))

    if model < 1 or model > 2:
        raise ValueError()

    cs.set_simulation(model, 2)

def get_p_simulation():
    print("Select model:")
    print("1. Standard")
    print("2. Better")
    print("3. Standard Scalability")
    print("4. Better Scalability")
    model = int(input("Select the number: "))

    if model < 1 or model > 4:
        raise ValueError()

    cs.set_simulation(model, 1)

