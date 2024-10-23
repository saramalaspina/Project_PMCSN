# # -------------------------------------------------------------------------
#  * This program is a next-event simulation of a single-server FIFO service
#  * node using Exponentially distributed interarrival times and Uniformly
#  * distributed service times (i.e., a M/U/1 queue).  The service node is
#  * assumed to be initially idle, no arrivals are permitted after the
#  * terminal time STOP, and the service node is then purged by processing any
#  * remaining jobs in the service node.
#  *
#  * Name            : ssq3.c  (Single Server Queue, version 3)
#  * Author          : Steve Park & Dave Geyer
#  * Language        : ANSI C
#  * Latest Revision : 10-19-98
#  # Translated by   : Philip Steele
#  # Language        : Python 3.3
#  # Latest Revision : 3/26/14
#  * -------------------------------------------------------------------------
#  */

from math import log
from libraries.rngs import plantSeeds, random, selectStream  # Multi-stream generator
from utils.constants import*

START = 0.0  # initial time
STOP = 86400.0  # terminal (close the door) time
INFINITY = (100.0 * STOP)  # must be much larger than STOP
arrivalTemp = START  # global temp var for getArrival function


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
    arrivalTemp += Exponential(1 / 1.4)
    return arrivalTemp


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



class Track:
    def __init__(self):
        self.node = 0.0  # time integrated number in the node
        self.queue = 0.0  # time integrated number in the queue
        self.service = 0.0  # time integrated number in service


class Time:
    def __init__(self):
        self.arrival = -1  # next arrival time
        self.completion_edge = -1  # next completion time for server 1
        self.completion_cloud = -1  # next completion time for server 2
        self.current = -1  # current time
        self.next = -1  # next (most imminent) event time
        self.last = -1  # last arrival time


##########################Main Program##################################

index_edge = 0  # used to count departed jobs from edge node
index_cloud = 0  # used to count departed jobs from cloud server

# Aggiungiamo variabili per contare i job che escono dal sistema
index_exit_E = 0  # used to count departed jobs of type E after first edge processing
index_exit_C = 0  # used to count departed jobs of type C after second edge processing

number_edge = 0  # number of jobs in server 1
number_cloud = 0  # number of jobs in server 2
area_edge = Track()  # stats tracking for server 1
area_cloud = Track()  # stats tracking for server 2
t = Time()

plantSeeds(123456789)

# Initialize times
t.current = START
t.arrival = GetArrival()  # First arrival for server 1
t.completion_edge = INFINITY  # No completions initially
t.completion_cloud = INFINITY  # No completions initially

# Simulation loop
queue_edge = []  # A list to track the type of jobs waiting at the edge node
queue_cloud = []  # A list to track jobs in the cloud queue
in_service_edge = False  # Edge node starts idle
in_service_cloud = False  # Cloud server starts idle

while (t.arrival < STOP) or (number_edge > 0) or (number_cloud > 0):
    t.next = Min(t.arrival, t.completion_edge, t.completion_cloud)  # Find next event

    # Update statistics for edge node
    if number_edge > 0:
        area_edge.node += (t.next - t.current) * number_edge
        area_edge.queue += (t.next - t.current) * (number_edge - 1)
        if in_service_edge:
            area_edge.service += (t.next - t.current)

    # Update statistics for cloud server
    if number_cloud > 0:
        area_cloud.node += (t.next - t.current) * number_cloud
        area_cloud.queue += (t.next - t.current) * (number_cloud - 1)
        if in_service_cloud:
            area_cloud.service += (t.next - t.current)

    t.current = t.next  # Advance the clock

    if t.current == t.arrival:  # Process arrival at edge node
        number_edge += 1
        queue_edge.append('E')  # New jobs are of type E at first
        t.arrival = GetArrival()  # Schedule next arrival
        if t.arrival > STOP:
            t.last = t.current
            t.arrival = INFINITY

        # If the edge server is idle, start serving the job immediately
        if not in_service_edge:
            job_type = queue_edge.pop(0)
            in_service_edge = True
            if job_type == 'E':
                t.completion_edge = t.current + GetServiceEdgeE()
            else:
                t.completion_edge = t.current + GetServiceEdgeC()

    elif t.current == t.completion_edge:  # Process completion at edge node
        if job_type == 'E':
            selectStream(3)  # Use a different stream for this decision
            if random() < P_C:  # With probability P_C, send job to cloud server
                number_cloud += 1
               # queue_cloud.append('C')  # Mark it as a type C job returning from cloud
                if not in_service_cloud:  # If cloud server is idle, start service
                    #job_type_cloud = queue_cloud.pop(0)
                    in_service_cloud = True
                    t.completion_cloud = t.current + GetServiceCloud()
            else:
                index_exit_E += 1  # Job of type E exits the system
        else:  # job_type == 'C'
            index_exit_C += 1  # Job of type C exits the system after second edge processing

        index_edge += 1
        number_edge -= 1
        in_service_edge = False

        if len(queue_edge) > 0:  # If there are jobs in the queue, serve the next one
            next_job_type = queue_edge.pop(0)
            in_service_edge = True
            if next_job_type == 'E':
                t.completion_edge = t.current + GetServiceEdgeE()
            else:
                t.completion_edge = t.current + GetServiceEdgeC()
        else:
            t.completion_edge = INFINITY

    elif t.current == t.completion_cloud:  # Process completion at cloud server (job becomes type C)
        index_cloud += 1
        number_cloud -= 1
        in_service_cloud = False

        if len(queue_cloud) > 0:  # If there are jobs in the cloud queue, serve the next one
            job_type_cloud = queue_cloud.pop(0)
            in_service_cloud = True
            t.completion_cloud = t.current + GetServiceCloud()
        else:
            t.completion_cloud = INFINITY

        # Job returns to edge node for final service (now type C)
        number_edge += 1
        queue_edge.append('C')  # Mark it as a type C job returning from cloud
        if not in_service_edge:  # If edge node is idle, start service
            job_type = queue_edge.pop(0)
            in_service_edge = True
            t.completion_edge = t.current + GetServiceEdgeC()


# End of simulation loop

# Output the statistics for edge node and cloud server
print(f"\nFor {index_edge} jobs processed by edge node (first and second pass):")
print(f"   Average interarrival time = {t.last / index_edge:.2f}")
print(f"   Average wait ............ = {area_edge.node / index_edge:.2f}")
print(f"   Average delay ........... = {area_edge.queue / index_edge:.2f}")
print(f"   Average service time .... = {area_edge.service / index_edge:.2f}")
print(f"   Average # in the node ... = {area_edge.node / t.current:.2f}")
print(f"   Average # in the queue .. = {area_edge.queue / t.current:.2f}")
print(f"   Utilization ............. = {area_edge.service / t.current:.2f}")

print(f"\nFor {index_cloud} jobs processed by cloud server:")
print(f"   Average wait ............ = {area_cloud.node / index_cloud:.2f}")
print(f"   Average delay ........... = {area_cloud.queue / index_cloud:.2f}")
print(f"   Average service time .... = {area_cloud.service / index_cloud:.2f}")
print(f"   Average # in the node ... = {area_cloud.node / t.current:.2f}")
print(f"   Average # in the queue .. = {area_cloud.queue / t.current:.2f}")
print(f"   Utilization ............. = {area_cloud.service / t.current:.2f}")

print(f"\nTotal jobs exited the system after first edge processing (type E): {index_exit_E}")
print(f"Total jobs exited the system after second edge processing (type C): {index_exit_C}")
