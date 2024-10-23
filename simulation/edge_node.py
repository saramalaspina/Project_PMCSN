from libraries import rngs
from simulation.queue_manager import QueueManager
from simulation.server import Server, release_server
from simulation.sim_utils import get_next_arrival_time, get_service_time
from utils.constants import*


rngs.plantSeeds(SEED)

queue_manager = QueueManager()

servers_edge = [Server() for _ in range(EDGE_SERVERS)]
arrived_job = 0
completed_job = 0

# Processa l'arrivo di un job all'edge node
def process_job_arrival_at_edge(t, servers_edge):
    print(f"Job arrived at edge node at time {t.current_time}")

    t.next_arrival = get_next_arrival_time(MEAN_ARRIVAL_TIME) + t.current_time

    # Controlla se il server è libero
    free_server = next((server for server in servers_edge if not server.occupied), None)
    if free_server:
        free_server.occupied = True
        free_server.start_service_time = t.current_time

        service_time = get_service_time('edge_node')
        free_server.end_service_time = t.current_time + service_time
        t.edge_completion = free_server.end_service_time
    else:
        queue_manager.add_to_queue('hub', t.current_time)

    update_completion_time(t)

def update_completion_time(t):
    t.edge_completion = min((server.end_service_time for server in servers_edge if server.occupied), default=INF)

def process_job_completion_at_edge(t):
    # server che ha completato il job
    completed_server = next((server for server in servers_edge if server.end_service_time == t.current_time), None)
    if completed_server:
        release_server(completed_server)

        print(f"Job in hub completed at time {t.current_time}")

        # ci sono job in coda
        if not queue_manager.is_queue_empty("edge_node"):
            next_job_time = queue_manager.get_from_queue('edge_node')

            completed_server.occupied = True
            completed_server.start_service_time = next_job_time

            service_time = get_service_time('edge_node')
            completed_server.end_service_time = t.current_time + service_time

        update_completion_time(t)

    update_completion_time(t)

def execute(t):
    events = {
        'arrival': t.next_arrival,
        'edge_completion': t.edge_completion,
    }

    next_event_time = min(t.next_arrival, t.edge_completion)
    t.current_time = next_event_time if next_event_time != INF else INF

    if t.current_time == t.next_arrival:
       # stats.increment_arrived_job()
        process_job_arrival_at_edge(t, servers_edge)

    elif t.current_time == t.edge_completion:
        process_job_completion_at_edge(t)

    # stats
   # stats.calculate_system_status(queue_manager, t.current_time, operative_servers, servers_hub)
   # stats.calculate_queues_status(queue_manager, t.current_time)

   # print_queue_status(queue_manager)



