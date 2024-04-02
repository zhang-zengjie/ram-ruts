import numpy as np
from commons.agent import Agent
from stlpy.systems import LinearSystem
from stlpy.benchmarks.common import inside_rectangle_formula, outside_rectangle_formula

SAFETY = (-10, 10, -2, 10)
HOME = (-10, 10, -2, 0)
TARGETA = (-10, -8, 8, 10)
TARGETB = (7, 9, 7, 9)
CHARGER = (-8, -3, 2, 4)
OBSTACLE = (-2, 2, 3, 10)

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

    # Input limits
    x0 = np.array([0, 0])

    spec0, _ = get_spec(n)

    agent = Agent(sys, spec0, N, x0, Q=Q, R=R, ub=2, name='agent')

    return agent

def get_spec(n):

    # Objectives (conjuctions/disjuntions of normalized half-spaces)
    gamma_S = inside_rectangle_formula(SAFETY, 0, 1, n)
    gamma_H = inside_rectangle_formula(HOME, 0, 1, n)
    gamma_TA = inside_rectangle_formula(TARGETA, 0, 1, n)
    gamma_TB = inside_rectangle_formula(TARGETB, 0, 1, n)
    gamma_C = inside_rectangle_formula(CHARGER, 0, 1, n)
    gamma_O = outside_rectangle_formula(OBSTACLE, 0, 1, n)

    # Single-Agent Version

    bar_phi_B = gamma_S.always(0, 40) & gamma_O.always(0, 40)
    bar_phi_T = gamma_TA.eventually(20, 30) | gamma_TB.eventually(20, 30)
    bar_phi_C = gamma_C.eventually(20, 25)
    bar_phi_H = gamma_H.always(0, 5).eventually(25, 30)

    bar_phi_B.name = "SAFETY"
    bar_phi_T.name = "GO TO TARGETS"
    bar_phi_C.name = "CHARGING"
    bar_phi_H.name = "GO HOME"

    times = [5, 15, 20]
    specs = [bar_phi_T, bar_phi_C, bar_phi_H]

    return bar_phi_B, (times, specs)