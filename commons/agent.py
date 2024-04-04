import numpy as np
from commons.functions import PRT, calculate_probabilities
from gurobipy import GRB
from probstlpy.solvers.gurobi.gurobi_micp import GurobiMICPSolver
import logging


class Agent:

    def __init__(self, sys, spec, N, x0, Q, R, ub, name):

        self.name = name
        self.N = N              # Time-horizon
        self.sys = sys

        self.psi = spec

        self.x0 = x0
        self.w = np.random.multivariate_normal(sys.mu, sys.Sigma, N).T
        # self.w = np.zeros([sys.n, N])  # uncomment to check with no disturbance

        self.Q = Q
        self.R = R

        # Compute 1) relation between tube and probability & 2) Stabilizing feedback gain
        self.diag_sigma_inf, self.K = PRT(self.sys, self.Q, self.R)

        # Initialize Memory
        self.xx = np.zeros([sys.n, self.N + 1])
        self.zz = np.zeros([sys.n, self.N + 1])

        self.xx[:, 0] = self.x0
        self.zz[:, 0] = self.x0

        self.z = np.zeros([sys.n, self.N + 1])
        self.zh = []
        
        self.err = np.zeros([sys.n, self.N + 1])
        self.vv = np.zeros([sys.m, self.N])
        self.v = np.zeros([sys.m, self.N])
        
        self.u_limits = np.array([[-ub, ub], [-ub, ub]])

        self.accept_meas = []

        # The lists of accepted specifications
        self.accept_phi = [spec]                                # Accepted specifications
        self.accept_prob = [np.ones((self.N, ))]                # Acceptance probabilities
        self.accept_time = [0]                                  # The time instants of acceptation

        self.risk = None
        self.x = None

        self.solver = GurobiMICPSolver(self.psi, self.sys, self.zz, self.N, self.diag_sigma_inf, uu=self.vv, riskH=self.risk, mark=0)
        self.solver.AddSTLConstraints(self.psi)
        self.solver.AddNewSTLProbConstraint(self.psi)
        self.solver.AddControlBounds(self.u_limits[:, 0], self.u_limits[:, 1])


    def update_measurement(self, t):
        self.zz[:, t] = self.xx[:, t]
        return None


    def update_probabilities(self, t):

        spec_prob = calculate_probabilities(self.accept_phi, self.risk)

        for i in range(len(self.accept_phi)):
            self.accept_prob[i][t] = spec_prob[i]
        return None
    

    def update_memory(self, t):

        # Update Memory
        self.zh += [self.z]
        if t == 0:
            self.err[:, 1] = self.w[:, 0]
        else:
            self.err[:, t + 1] = (self.sys.A - self.sys.B @ self.K) @ self.err[:, t] + self.w[:, t]
        self.xx[:, t + 1] = self.z[:, t + 1] + self.err[:, t + 1]
        self.vv[:, t] = self.v[:, t]

        return None


    def probe_task(self, t, spec=None):

        self.solver.mark = t
        self.solver.riskH = self.risk

        if spec is not None:
            STLConstrs = self.solver.AddSTLConstraints(spec)
            STLProbConstrs = self.solver.AddNewSTLProbConstraint(spec)
            
        DynConstrs = self.solver.AddDynamicsConstraints()
        RiskConstrs = self.solver.AddRiskConstraints()
        
        self.solver.AddRiskCost()
        self.solver.AddQuadraticInputCost(self.R)
        z, v, risk, flag, _ = self.solver.Solve()

        self.solver.model.remove(DynConstrs)
        self.solver.model.remove(RiskConstrs)

        if spec is not None:
            self.solver.model.remove(STLConstrs)
            self.solver.model.remove(STLProbConstrs)

        self.solver.model.update()

        return (z, v, risk, flag)           


    def accept_task(self, t, spec):

        self.psi = self.psi & spec
        self.accept_phi += [spec]
        self.accept_prob += [np.ones((self.N, ))]
        self.accept_time += [t]
        self.solver.AddSTLConstraints(spec)
        self.solver.AddNewSTLProbConstraint(spec)

        logging.info(self.name + " has accepted the new task " + spec.name + " at step " + str(t) + "!")


    def reject_task(self, t, spec):
        
        logging.info(self.name + " has rejected the new task " + spec.name + " at step " + str(t) + "!")


    def apply_control(self, t, solution):

        
        #solver.AddControlBounds(self.u_limits[:, 0], self.u_limits[:, 1])
        #solver.AddQuadraticInputCost(self.R)
        zNew, vNew, riskNew, flag = solution

        # Check whether a solution has been found!
        if flag != GRB.OPTIMAL:

            self.zz[:, t] = self.z[:, t]
            logging.info(self.name + " has rejected the new measurement at step " + str(t) + "!")

        else:
            # Update control strategy
            self.z = zNew
            self.v = vNew
            self.risk = riskNew
            self.err[:, t] = 0
            self.accept_meas += [t]
            
            logging.info(self.name + " has accepted the new measurement at step " + str(t) + "!")
        
        self.update_memory(t)
        self.update_probabilities(t)
        self.update_measurement(t+1)
