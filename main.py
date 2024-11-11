from simulation.simulator import finite_simulation
from utils.constants import *

if SIMULATION_TYPE == FINITE:
    n_run = REPLICATIONS
elif SIMULATION_TYPE == INFINITE:
    n_run = K
else:
    print("TYPE not valid!")
    exit(1)


for i in range(n_run):
    if SIMULATION_TYPE == FINITE:
        finite_simulation()
    elif SIMULATION_TYPE == INFINITE:
        print("To do")
    else:
        print("Invalid simulation type!")
        break