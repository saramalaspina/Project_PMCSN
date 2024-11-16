def print_edge_stats(stats):
    print(f"\nFor {stats.index_edge} jobs processed by edge node (first and second pass):")
    print(f"   Average wait ............ = {stats.area_edge.node / stats.index_edge:.2f}")
    print(f"   Average delay ........... = {stats.area_edge.queue / stats.index_edge:.2f}")
    print(f"   Average service time .... = {stats.area_edge.service / stats.index_edge:.2f}")
    print(f"   Average # in the node ... = {stats.area_edge.node / stats.t.current:.2f}")
    print(f"   Average # in the queue .. = {stats.area_edge.queue / stats.t.current:.2f}")
    print(f"   Utilization ............. = {stats.area_edge.service / stats.t.current:.2f}")
    print(f"   Average interarrival time = {stats.t.last / stats.index_edge:.2f}")

def print_cloud_stats(stats):
    if stats.index_cloud > 0:
        print(f"\nFor {stats.index_cloud} jobs processed by cloud server:")
        print(f"   Average wait ............ = {stats.area_cloud.node / stats.index_cloud:.2f}")
        print(f"   Average delay ........... = {stats.area_cloud.queue / stats.index_cloud:.2f}")
        print(f"   Average service time .... = {stats.area_cloud.service / stats.index_cloud:.2f}")
        print(f"   Average # in the node ... = {stats.area_cloud.node / stats.t.current:.2f}")
        print(f"   Average # in the queue .. = {stats.area_cloud.queue / stats.t.current:.2f}")
        print(f"   Utilization ............. = {stats.area_cloud.service / stats.t.current:.2f}")

def print_type_E_stats(stats):
    print(f"\nFor {stats.index_E} type E jobs processed by edge node:")
    print(f"   Average wait ............ = {stats.area_E.node / stats.index_E:.2f}")
    print(f"   Average delay ........... = {stats.area_E.queue / stats.index_E:.2f}")
    print(f"   Average service time .... = {stats.area_E.service / stats.index_E:.2f}")
    print(f"   Average # in the node ... = {stats.area_E.node / stats.t.current:.2f}")
    print(f"   Average # in the queue .. = {stats.area_E.queue / stats.t.current:.2f}")
    print(f"   Utilization ............. = {stats.area_E.service / stats.t.current:.2f}")

def print_type_C_stats(stats):
    if stats.index_C > 0:
        print(f"\nFor {stats.index_C} type C jobs in edge node:")
        print(f"   Average wait ............ = {stats.area_C.node / stats.index_C:.2f}")
        print(f"   Average delay ........... = {stats.area_C.queue / stats.index_C:.2f}")
        print(f"   Average service time .... = {stats.area_C.service / stats.index_C:.2f}")
        print(f"   Average # in the node ... = {stats.area_C.node / stats.t.current:.2f}")
        print(f"   Average # in the queue .. = {stats.area_C.queue / stats.t.current:.2f}")
        print(f"   Utilization ............. = {stats.area_C.service / stats.t.current:.2f}")

def print_job_counts(stats):
    print(f"\nNumber of type E jobs that leave the system = {stats.count_E}")
    print(f"Number of type C jobs that leave the system = {stats.count_C}")

def print_all_stats(stats):
    print_edge_stats(stats)
    print_cloud_stats(stats)
    print_type_E_stats(stats)
    print_type_C_stats(stats)
    print_job_counts(stats)
