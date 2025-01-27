LAMBDA = 1.65 # mean arrival time [secondo/job]

EDGE_SERVERS = 1
CLOUD_SERVERS = 1

EDGE_SERVERS_MAX = 3
CLOUD_SERVERS_MAX = 3

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

REPLICATIONS = 96

INFINITE = 0
FINITE = 1
SIMULATION_TYPE = FINITE

BETTER = 0
STANDARD = 1
SCALABILITY = 2
BETTER_SCALABILITY = 3
MODEL = SCALABILITY

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

PRINT_PLOT_TIME = 0
PRINT_PLOT_BATCH = 1

PRINT_AUTOCORRELATION = 1

def set_transient_analysis(model):
    global TRANSIENT_ANALYSIS, REPLICATIONS, SIMULATION_TYPE, P_C, LAMBDA, MODEL
    TRANSIENT_ANALYSIS = 1
    REPLICATIONS = 7
    SIMULATION_TYPE = FINITE
    P_C = 0.4
    LAMBDA = 1.4
    if model == 1:
        MODEL = STANDARD
    elif model == 2:
        MODEL = BETTER
    else:
        raise ValueError()

def set_simulation(model, sim_type):
    global SIMULATION_TYPE, MODEL
    if model == 1:
        MODEL = STANDARD
    elif model == 2:
        MODEL = BETTER
    elif model == 3:
        MODEL = SCALABILITY
    else:
        MODEL = BETTER_SCALABILITY

    if sim_type == 1:
        SIMULATION_TYPE = FINITE
    else:
        SIMULATION_TYPE = INFINITE

def set_lambda(value):
    global LAMBDA
    LAMBDA = value

def set_autocorrelation(value):
    global PRINT_AUTOCORRELATION
    PRINT_AUTOCORRELATION = value


