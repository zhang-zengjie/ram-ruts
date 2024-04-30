import numpy as np
from gurobipy import GRB
from commons.functions import config_logger
from commons.configs import get_agent, get_spec
from commons.plot_fig import plot_fig
import logging

seed = 3                # Set random seed
np.random.seed(seed)
N = 40                  # Time-horizon
n = 2                   # System dimension

agent = get_agent(n, N)
_, lists = get_spec(n)
times, specs = lists

config_logger(logging, 'INFO.log')
for t in range(N):

    if t in times:
        new_task = specs[times.index(t)]
        sln = agent.probe_task(t, new_task)
        if sln[-1] != GRB.OPTIMAL:
                agent.reject_task(t, new_task)
        agent.accept_task(t, new_task)

    agent.apply_control(t, agent.probe_task(t))

plot_fig(agent)
