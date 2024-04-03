import numpy as np
from gurobipy import GRB
from commons.functions import config_logger
from configs import get_agent, get_spec
import logging

seed = 3                # Set random seed
np.random.seed(seed)
N = 40                  # Time-horizon
n = 2                   # System dimension

agent = get_agent(n, N)
_, lists = get_spec(n)
times, specs = lists


config_logger(logging, 'data/INFO.log')
for t in range(N):

    if t in times:
        new_task = specs[times.index(t)]
        sln = agent.probe_task(t, new_task)
        if sln[-1] != GRB.OPTIMAL:
                agent.reject_task(t)
        agent.accept_task(t, new_task)

    agent.apply_control(t, agent.probe_task(t))

# Save Memory
np.save('data/' + agent.name + '_prob.npy', agent.accept_prob)
np.save('data/' + agent.name + '_accepted_time.npy', agent.accept_time)
np.save('data/' + agent.name + '_meas_state.npy', agent.xx)
np.save('data/' + agent.name + '_hist_nom_state.npy', agent.zh)
