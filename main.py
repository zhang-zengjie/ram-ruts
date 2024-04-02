import numpy as np
from config.specs import time_list_single, spec_list_single
from config.params import N, agent
from gurobipy import GRB
from commons.functions import config_logger
import logging


config_logger(logging, 'data/single/INFO.log')
for t in range(N):

    if t in time_list_single:
        new_task = spec_list_single[time_list_single.index(t)]
        sln = agent.probe_task(t, new_task)
        if sln[-1] != GRB.OPTIMAL:
                agent.reject_task(t)
        agent.accept_task(t, new_task)

    agent.apply_control(t, agent.probe_task(t))

# Save Memory
np.save('data/single/' + agent.name + '_prob.npy', agent.accept_prob)
np.save('data/single/' + agent.name + '_accepted_time.npy', agent.accept_time)
np.save('data/single/' + agent.name + '_meas_state.npy', agent.xx)
np.save('data/single/' + agent.name + '_hist_nom_state.npy', agent.zh)
