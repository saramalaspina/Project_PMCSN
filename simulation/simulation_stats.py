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

class SimulationStats:
    def __init__(self):
        self.job_arrived = 0 # used to count arrived jobs

        self.index_edge = 0 # used to count departed jobs from edge node
        self.index_cloud = 0 # used to count departed jobs from cloud server
        self.count_E = 0 # number of type E departed jobs
        self.count_C = 0 # number of type C departed jobs

        self.number_edge = 0 # number of jobs in server 1
        self.number_cloud = 0 # number of jobs in server 2
        self.number_E = 0 # number of type E jobs in edge node
        self.number_C = 0 # number of type C jobs in edge node
        self.index_E = 0 # number of type E processed jobs in edge node
        self.index_C = 0 # number of type C processed jobs in edge node
        self.queue_edge_E = 0 # number of type E in edge queue for better simulation
        self.queue_edge_C = 0 # number of type C in edge queue for better simulation

        # Tracciamento delle aree per statistiche
        self.area_edge = Track() # stats tracking for server 1
        self.area_cloud = Track() # stats tracking for server 2
        self.area_E = Track() # stats tracking job of type E
        self.area_C = Track() # stats tracking job of type C in edge node

        # Variabile per i tempi
        self.t = Time()
        self.queue_edge = [] # A list to track the type of jobs waiting at the edge node

    def reset(self, start_time):
        self.t.current = start_time
        self.t.completion_edge = float('inf')
        self.t.completion_cloud = float('inf')
        self.queue_edge.clear()  # Svuota la coda

    def reset_infinite(self):
        self.job_arrived = 0  # used to count arrived jobs

        self.index_edge = 0  # used to count departed jobs from edge node
        self.index_cloud = 0  # used to count departed jobs from cloud server
        self.count_E = 0  # number of type E departed jobs
        self.count_C = 0  # number of type C departed jobs

        self.index_E = 0  # number of type E processed jobs in edge node
        self.index_C = 0  # number of type C processed jobs in edge node

        self.area_edge = Track()  # stats tracking for server 1
        self.area_cloud = Track()  # stats tracking for server 2
        self.area_E = Track()  # stats tracking job of type E
        self.area_C = Track()  # stats tracking job of type C in edge node

    def calculate_area_queue(self):
        self.area_edge.queue = self.area_edge.node - self.area_edge.service
        self.area_cloud.queue = self.area_cloud.node - self.area_cloud.service
        self.area_E.queue = self.area_E.node - self.area_E.service
        self.area_C.queue = self.area_C.node - self.area_C.service

class ReplicationStats:
    def __init__(self):
        self.edge_num_server = []

        self.edge_wait_times = []
        self.edge_delays = []
        self.edge_service_times = []
        self.edge_utilization = []
        self.edge_number_node = []
        self.edge_number_queue = []

        # lists for cloud stats
        self.cloud_wait_times = []
        self.cloud_delays = []
        self.cloud_service_times = []
        self.cloud_utilization = []
        self.cloud_number_node = []
        self.cloud_number_queue = []

        # lists for E type job stats
        self.E_jobs_leaving = []
        self.E_edge_wait_times = []
        self.E_edge_delays = []
        self.E_edge_service_times = []
        self.E_edge_utilization = []
        self.E_edge_number_node = []
        self.E_edge_number_queue = []

        # lists for C type job stats
        self.C_jobs_leaving = []
        self.C_edge_wait_times = []
        self.C_edge_delays = []
        self.C_edge_service_times = []
        self.C_edge_utilization = []
        self.C_edge_number_node = []
        self.C_edge_number_queue = []


