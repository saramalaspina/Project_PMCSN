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
    arrivalTemp += Exponential(1 / MEAN_ARRIVAL_TIME)
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

count_E = 0 # number of type E departed jobs
count_C = 0 # number of type C departed jobs

number_edge = 0  # number of jobs in server 1
number_cloud = 0  # number of jobs in server 2
number_E = 0 # number of type E jobs in edge node
number_C = 0 # number of type C jobs in edge node
index_E = 0 # number of type E processed jobs in edge node
index_C = 0 # number of type C processed jobs in edge node
area_edge = Track()  # stats tracking for server 1
area_cloud = Track()  # stats tracking for server 2
area_E = Track() # stats tracking job of type E
area_C = Track() # stats tracking job of type C in edge node
t = Time()

plantSeeds(123456789)

# Initialize times
t.current = START
t.arrival = GetArrival()  # First arrival for server 1
t.completion_edge = INFINITY  # No completions initially
t.completion_cloud = INFINITY  # No completions initially

queue_edge = []  # A list to track the type of jobs waiting at the edge node

# Simulation loop
while (t.arrival < STOP) or (number_edge + number_cloud > 0):
    t.next = Min(t.arrival, t.completion_edge, t.completion_cloud)  # next event time   */

    if (number_edge > 0):  # update integrals  */
        area_edge.node += (t.next - t.current) * number_edge
        area_edge.queue += (t.next - t.current) * (number_edge - 1)
        area_edge.service += (t.next - t.current)
    # EndIf

    if (number_cloud > 0):  # update integrals  */
        area_cloud.node += (t.next - t.current) * number_cloud
        area_cloud.queue += (t.next - t.current) * (number_cloud - 1)
        area_cloud.service += (t.next - t.current)
    # EndIf

    if (number_E > 0):  # update integrals  */
        area_E.node += (t.next - t.current) * number_E
        area_E.queue += (t.next - t.current) * (number_E - 1)
        area_E.service += (t.next - t.current)
    # EndIf

    if (number_C > 0):  # update integrals  */
        area_C.node += (t.next - t.current) * number_C
        area_C.queue += (t.next - t.current) * (number_C - 1)
        area_C.service += (t.next - t.current)
    # EndIf

    t.current = t.next  # advance the clock */

    if (t.current == t.arrival):  # process an arrival */
        number_edge += 1
        number_E += 1
        queue_edge.append("E")
        t.arrival = GetArrival()
        if (t.arrival > STOP):
            t.last = t.current
            t.arrival = INFINITY

        if (number_edge == 1):
            t.completion_edge = t.current + GetServiceEdgeE()

    elif t.current == t.completion_edge: # Process completion at edge node
        if queue_edge[0] == "E":  # The job has not returned yet
            number_E -=1
            index_E += 1
            selectStream(3)
            if random() < P_C:  # With probability p, send job to server 2
                number_cloud += 1
                if number_cloud == 1:  # If server 2 is idle, start service
                    t.completion_cloud = t.current + GetServiceCloud()
            else:
                count_E += 1
        else:
            count_C +=1
            index_C += 1
            number_C -=1

        index_edge += 1
        number_edge -= 1
        queue_edge.pop(0)
        if number_edge > 0:
            if queue_edge[0] == "E":
                t.completion_edge = t.current + GetServiceEdgeE()
            else:
                t.completion_edge = t.current + GetServiceEdgeC()
        else:
            t.completion_edge = INFINITY

    elif t.current == t.completion_cloud:  # Process completion at cloud server
        index_cloud += 1
        number_cloud -= 1
        if number_cloud > 0:
            t.completion_cloud = t.current + GetServiceCloud()
        else:
            t.completion_cloud = INFINITY

        number_edge += 1
        number_C += 1
        queue_edge.append("C")
        if number_edge == 1:  # If edge node is idle, start service
            t.completion_edge = t.current + GetServiceEdgeC()

# EndWhile

# Output the statistics for edge node and cloud server
print(f"\nFor {index_edge} jobs processed by edge node (first and second pass):")
print(f"   Average wait ............ = {area_edge.node / index_edge:.2f}")
print(f"   Average delay ........... = {area_edge.queue / index_edge:.2f}")
print(f"   Average service time .... = {area_edge.service / index_edge:.2f}")
print(f"   Average # in the node ... = {area_edge.node / t.current:.2f}")
print(f"   Average # in the queue .. = {area_edge.queue / t.current:.2f}")
print(f"   Utilization ............. = {area_edge.service / t.current:.2f}")
print(f"   Average interarrival time = {t.last / index_edge:.2f}")

if(index_cloud > 0):
    print(f"\nFor {index_cloud} jobs processed by cloud server:")
    print(f"   Average wait ............ = {area_cloud.node / index_cloud:.2f}")
    print(f"   Average delay ........... = {area_cloud.queue / index_cloud:.2f}")
    print(f"   Average service time .... = {area_cloud.service / index_cloud:.2f}")
    print(f"   Average # in the node ... = {area_cloud.node / t.current:.2f}")
    print(f"   Average # in the queue .. = {area_cloud.queue / t.current:.2f}")
    print(f"   Utilization ............. = {area_cloud.service / t.current:.2f}")

print(f"\nFor {index_E} type E jobs processed by edge node:")
print(f"   Average wait ............ = {area_E.node / index_E:.2f}")
print(f"   Average delay ........... = {area_E.queue / index_E:.2f}")
print(f"   Average service time .... = {area_E.service / index_E:.2f}")
print(f"   Average # in the node ... = {area_E.node / t.current:.2f}")
print(f"   Average # in the queue .. = {area_E.queue / t.current:.2f}")
print(f"   Utilization ............. = {area_E.service / t.current:.2f}")

if(index_C>0):
    print(f"\nFor {index_C} type C jobs in edge node:")
    print(f"   Average wait ............ = {area_C.node / index_C:.2f}")
    print(f"   Average delay ........... = {area_C.queue / index_C:.2f}")
    print(f"   Average service time .... = {area_C.service / index_C:.2f}")
    print(f"   Average # in the node ... = {area_C.node / t.current:.2f}")
    print(f"   Average # in the queue .. = {area_C.queue / t.current:.2f}")
    print(f"   Utilization ............. = {area_C.service / t.current:.2f}")

print(f"\nNumber of type E jobs that leave the system = {count_E}")
print(f"Number of type C jobs that leave the system = = {count_C}")
