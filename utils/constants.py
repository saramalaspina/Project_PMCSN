INF = float('inf')

MEAN_ARRIVAL_TIME = 1.55  # Tempo medio di arrivo dei job [secondo/job]

EDGE_SERVERS = 1

P_C = 0.4

# Seeds per la generazione casuale
seeds = {
    "1": 324516786,
    "2": 140620017,
    "3": 170920015,
    "4": 170520018
}
SEED = seeds["1"]
SEED_INDEX = list(seeds.keys())[list(seeds.values()).index(SEED)]

REPLICATIONS = 2

INFINITE = 0

FINITE = 1

SIMULATION_TYPE = FINITE

K = 0
B = 0