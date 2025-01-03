LAMBDA = 1.55  # mean arrival time [secondo/job]

EDGE_SERVERS = 1
CLOUD_SERVERS = 1

EDGE_SERVERS_MAX = 2
CLOUD_SERVERS_MAX = 2

def increment_edge():
    global EDGE_SERVERS
    EDGE_SERVERS += 1

def decrement_edge():
    global EDGE_SERVERS
    EDGE_SERVERS -= 1

def increment_cloud():
    global CLOUD_SERVERS
    CLOUD_SERVERS += 1

def decrement_cloud():
    global CLOUD_SERVERS
    CLOUD_SERVERS -= 1

def set_servers(edge_num, cloud_num):
    global EDGE_SERVERS, CLOUD_SERVERS
    EDGE_SERVERS = edge_num
    CLOUD_SERVERS = cloud_num

P_C = 0.4

def set_probability(value):
    global P_C
    if value < 0 or value > 1:
        return ValueError()
    P_C = value

SEED = 123456789

REPLICATIONS = 7

INFINITE = 0
FINITE = 1
SIMULATION_TYPE = FINITE

BETTER = 0
STANDARD = 1
SCALABILITY = 2
BETTER_SCALABILITY = 3
MODEL = BETTER

START = 0.0  # initial time
STOP = 86400  # terminal (close the door) time
STOP_ANALYSIS = 300000
STOP_INFINITE = float('inf')
INFINITY = float('inf')  # must be much larger than STOP

EXPONENTIAL = 0
TRUNCATED_NORMAL = 1
SERVICE_DISTRIBUTION = EXPONENTIAL

TRANSIENT_ANALYSIS = 0

ALPHA = 0.05 # 95% confidence

K = 128
B = 4080