import numpy as np
from commons.agent import Agent
from stlpy.systems import LinearSystem
from config.specs import bar_phi_B as init_spec


seed = 3                # Set seed
np.random.seed(seed)
N = 40                  # Time-horizon

# System dynamics
n = 2
A = np.eye(n)
B = np.eye(n)
C = np.eye(n)
D = np.zeros([n, n])

# Disturbance variables
mu = np.zeros(n)
Sigma = 0.002 * np.eye(n)

# Initialize System
sys = LinearSystem(A, B, C, D, mu, Sigma)

# Quadratic Cost function (nonzero & SPD)
Q = np.eye(sys.n) * 0.001
R = np.eye(sys.m) * 0.001

# Input limits
x0 = np.array([0, 0])

agent = Agent(sys, init_spec, N, x0, Q=Q, R=R, ub=2, name='agent')