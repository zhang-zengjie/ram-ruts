import numpy as np
from commons.agent import Agent
from probstlpy.systems.linear import LinearSystem
from probstlpy.benchmarks.common import inside_rectangle_formula, outside_rectangle_formula

# The coordinates of the rectangular regions
# Each item -> 'REGION NAME': (x_min, x_max, y_min, y_max)
RG = {
    'WS': (-10, 10, -2, 10),            # The workspace
    'HOME': (-10, 10, -2, 0),           # The home region
    'TARGET-A': (-10, -8, 8, 10),       # The target A
    'TARGET-B': (7, 9, 7, 9),           # The target B
    'CHARGER': (-8, -3, 2, 4),          # The charger
    'OBSTACLE': (-2, 2, 3, 10)          # The obstacle
}

# The color map of the rectangular regions
# Each item -> 'REGION NAME': color vector in RGB
CM = {
    'WS': [0.8, 0.9, 1],                # The workspace
    'HOME': [0.3, 1, 0.4],              # The home region
    'TARGET-A': [1, 1, 0.3],            # The target A
    'TARGET-B': [1, 1, 0.3],            # The target B
    'CHARGER': [0, 0.5, 1],             # The charger
    'OBSTACLE': [1, 0.3, 0.3]           # The obstacle
}


def get_agent(n, N):

    # System dynamics
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

    # Set the initial state
    x0 = np.array([0, 0])

    # Get the initial specification
    spec0, _ = get_spec(n)

    agent = Agent(sys, spec0, N, x0, Q=Q, R=R, ub=2, name='agent')

    return agent

def get_spec(n):

    # Objectives (conjuctions/disjuntions of normalized half-spaces)
    gamma_S = inside_rectangle_formula(RG['WS'], 0, 1, n)
    gamma_H = inside_rectangle_formula(RG['HOME'], 0, 1, n)
    gamma_TA = inside_rectangle_formula(RG['TARGET-A'], 0, 1, n)
    gamma_TB = inside_rectangle_formula(RG['TARGET-B'], 0, 1, n)
    gamma_C = inside_rectangle_formula(RG['CHARGER'], 0, 1, n)
    gamma_O = outside_rectangle_formula(RG['OBSTACLE'], 0, 1, n)

    bar_phi_B = gamma_S.always(0, 40) & gamma_O.always(0, 40)
    bar_phi_T = gamma_TA.eventually(20, 30) | gamma_TB.eventually(20, 30)
    bar_phi_C = gamma_C.eventually(20, 25)
    bar_phi_H = gamma_H.always(0, 5).eventually(25, 30)

    bar_phi_B.name = "SAFETY"
    bar_phi_T.name = "GO TO TARGETS"
    bar_phi_C.name = "CHARGING"
    bar_phi_H.name = "GO HOME"

    # The run-time specifications and the corresponding times
    times = [5, 15, 20]                         # The time instants where run-time tasks are specified
    specs = [bar_phi_T, bar_phi_C, bar_phi_H]   # Run-time specifications

    return bar_phi_B, (times, specs)