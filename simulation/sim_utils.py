from libraries import rngs, rvms

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




