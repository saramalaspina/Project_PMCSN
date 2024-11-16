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





