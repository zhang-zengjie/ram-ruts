from ..base import STLSolver
from ...STL.predicate import LinearPredicate, NonlinearPredicate
import numpy as np

import gurobipy as gp
from gurobipy import GRB

import time

class GurobiMICPSolver(STLSolver):
    """
    Given an :class:`.STLFormula` :math:`\\varphi` and a :class:`.LinearSystem`,
    solve at time zero the optimization problem

    .. math::

        \min & \sum_{t=0}^T risk_t + \sum_{t=0}^T x_t^TQx_t + u_t^TRu_t

        \\text{s.t. } & x_0 \\text{ fixed}

        & x_{t+1} = A x_t + B u_t

        & \\rho^{\\varphi}(y_0,y_1,\dots,y_T) \geq 0

        & risk_t = 1 - af \\rho_t - bf

    with Gurobi using mixed-integer convex programming. This gives a globally optimal
    solution, but may be computationally expensive for long and complex specifications.
    
    .. note::

        This class implements the algorithm described in

        Belta C, et al.
        *Formal methods for control synthesis: an optimization perspective*.
        Annual Review of Control, Robotics, and Autonomous Systems, 2019.
        https://dx.doi.org/10.1146/annurev-control-053018-023717.

Mandatory
    :param spec:            A list of :class:`.STLFormula` describing the specification.
    :param sys:             A :class:`.LinearSystem` describing the system dynamics.
    :param xx:              A ``(n,T+1)`` numpy matrix containing the history of state.
    :param T:               A positive integer fixing the total number of time-steps :math:`T`.
    :param alpha:           A positive integer relating the rho and the risk:
                            risk = 1-\frac{rho-n*alpha}{rho}.

Optional
    :param beta:            A value between 0 and 1 to indicate the second
                            intersection between the over-approximated linear and exact
                            non-linear relation between rho and risk.
    :param uu:              A ``(m,T)`` numpy matrix containing the history of input.
    :param riskH:           A numpy array containing the history of risk.
    :param mark:            A mark indicating the current iteration. Default is ``0``.
    :param M:               A large positive scalar used to rewrite ``min`` and ``max`` as
                            mixed-integer constraints. Default is ``1000``.
    :param presolve:        A boolean indicating whether to use Gurobi's
                            presolve routines. Default is ``True``.
    :param verbose:         A boolean indicating whether to print detailed
                            solver info. Default is ``False``.
    """

    def __init__(self, spec, sys, xx, T, alpha,
                 beta=0.01, uu=None, riskH=None, mark=0,
                 M=1000, presolve=True, verbose=False):
        assert M > 0, "M should be a (large) positive scalar"
        super().__init__(None, sys, xx[:, 0], T, verbose)

        self.M = float(M)
        self.presolve = presolve
        self.model = gp.Model("STL_MICP")

        # Set up the optimization problem (Mandatory)
        self.xx = xx
        self.alpha = alpha

        # Set up the optimization problem (Optional)
        self.beta = beta
        self.uu = uu
        self.riskH = riskH
        self.mark = mark

        # Store the cost function, which will be added to self.model right before solving
        self.cost = 0.0

        # Set some model parameters
        if not self.presolve:
            self.model.setParam('Presolve', 0)
        if not self.verbose:
            self.model.setParam('OutputFlag', 0)

        if self.verbose:
            print("Setting up optimization problem...")
            st = time.time()  # for computing setup time

        # Create optimization variables
        self.x = self.model.addMVar((self.sys.n, self.T + 1), lb=-float('inf'), name='x')
        self.u = self.model.addMVar((self.sys.m, self.T), lb=-float('inf'), name='u')
        self.rho = self.model.addMVar((self.T + 1, ), name="rho", lb=0.0) # lb sets minimum robustness
        self.risk = self.model.addMVar((self.T + 1, ), name="risk")

        if self.verbose:
            print(f"Setup complete in {time.time()-st} seconds.")

# Optional Bounds and Costs
    def AddControlBounds(self, u_min, u_max):
        self.model.update()
        ExistingConstrs = self.model.getConstrs()

        for t in range(self.T):
            self.model.addConstr( u_min <= self.u[:, t] , name=f"ControlBoundsUB{t}")
            self.model.addConstr( self.u[:, t] <= u_max, name=f"ControlBoundsLB{t}" )
        
        self.model.update()
        NewConstrs = self.model.getConstrs()[len(ExistingConstrs):]
        return NewConstrs

    def AddStateBounds(self, x_min, x_max):
        self.model.update()
        ExistingConstrs = self.model.getConstrs()

        for t in range(self.T+1):
            self.model.addConstr( x_min <= self.x[:, t] ,name=f"XBoundsUB{t}")
            self.model.addConstr( self.x[:, t] <= x_max ,name=f"XBoundsLB{t}")

        self.model.update()
        NewConstrs = self.model.getConstrs()[len(ExistingConstrs):]
        return NewConstrs

    def AddNewSTLProbConstraint(self, formula):
        self.model.update()
        ExistingConstrs = self.model.getConstrs()

        mat = np.zeros(self.T+1)
        for j in formula.ts:
            mat[j] = 1
        self.model.addConstr(mat.T @ self.risk <= 1 - formula.prob, name="NewSTLProbBound")

        self.model.update()
        NewConstrs = self.model.getConstrs()[len(ExistingConstrs):]
        return NewConstrs

    def AddSTLProbConstraintSimple(self, formulas):
        self.model.update()
        ExistingConstrs = self.model.getConstrs()

        prob = max([formula.prob for formula in formulas])
        for i in range(len(formulas)):
            mat = np.zeros(self.T+1)
            for j in formulas[i].ts:
                mat[j] = 1
            self.model.addConstr(mat.T @ self.risk <= 1 - prob, name=f"STLProbBound{i}")

        self.model.update()
        NewConstrs = self.model.getConstrs()[len(ExistingConstrs):]
        return NewConstrs

    def AddSTLProbConstraintComplex(self, formulas):
        self.model.update()
        ExistingConstrs = self.model.getConstrs()

        for i in range(len(formulas)):
            mat = np.zeros(self.T+1)
            for j in formulas[i].ts:
                mat[j] = 1
            self.model.addConstr(mat.T @ self.risk <= 1 - formulas[i].prob, name=f"STLProbBound{i}")

        self.model.update()
        NewConstrs = self.model.getConstrs()[len(ExistingConstrs):]
        return NewConstrs

    # Mandatory Bounds and Costs
    def AddDynamicsConstraints(self):

        self.model.update()
        ExistingConstrs = self.model.getConstrs()

        # Initial condition
        self.model.addConstr(self.x[:, 0] == self.xx[:, 0],name="x_xx0")

        # Fixed state and input
        if self.mark > 0:
            for t in range(1, self.mark+1):
                self.model.addConstr(self.x[:, t] == self.xx[:, t] ,name=f"x_xx{t}")
                self.model.addConstr(self.u[:, t-1] == self.uu[:, t-1],name=f"u_uu{t-1}")

        # Dynamics
        for t in range(self.mark, self.T):
            self.model.addConstr(
                    self.x[:, t+1] == self.sys.A@self.x[:, t] + self.sys.B@self.u[:, t], name=f"x({t}+1)_AxBu" )

        self.model.update()
        NewConstrs = self.model.getConstrs()[len(ExistingConstrs):]
        return NewConstrs
    

    def AddRiskConstraints(self):

        self.model.update()
        ExistingConstrs = self.model.getConstrs()

        for risk in self.risk:
            self.model.addConstr(risk >= self.beta)
            self.model.addConstr(risk <= 1.0)

        # Calculate linear function that upper bounds the relation between rho and risk
        af = -(self.beta) / (self.sys.n * self.alpha)
        bf = 1 + self.beta

        # Constraint history of risk
        if self.mark > 0:
            for i in range(self.mark + 1):
                self.model.addConstr(self.risk[i] == self.riskH[i],name=f"R_RH{i}")

        # Constraint relation between risk and rho
        for i in range(self.T + 1):
            self.model.addConstr(self.risk[i] == af*self.rho[i]*self.rho[i] + bf,name=f"R_rho{i}")

        self.model.update()
        NewConstrs = self.model.getConstrs()[len(ExistingConstrs):]
        return NewConstrs


    def AddSTLConstraints(self, spec):
        """
        Add the STL constraints

            (x,u) |= specification

        to the optimization problem, via the recursive introduction
        of binary variables for all subformulas in the specification.
        """
        # Recursively traverse the tree defined by the specification
        # to add binary variables and constraints that ensure that
        # rho is the robustness value

        self.model.update()
        ExistingConstrs = self.model.getConstrs()

        z_spec = self.model.addMVar(1,vtype=GRB.CONTINUOUS)
        self.AddSubformulaConstraints(spec, z_spec, 0)
        self.model.addConstr( z_spec == 1 )

        self.model.update()
        NewConstrs = self.model.getConstrs()[len(ExistingConstrs):]
        return NewConstrs
    

    def AddSubformulaConstraints(self, formula, z, t):
        """
        Given an STLFormula (formula) and a binary variable (z),
        add constraints to the optimization problem such that z
        takes value 1 only if the formula is satisfied (at time t).

        If the formula is a predicate, this constraint uses the "big-M"
        formulation

            A[x(t);u(t)] - b + (1-z)M >= 0,

        which enforces A[x;u] - b >= 0 if z=1, where (A,b) are the
        linear constraints associated with this predicate.

        If the formula is not a predicate, we recursively traverse the
        subformulas associated with this formula, adding new binary
        variables z_i for each subformula and constraining

            z <= z_i  for all i

        if the subformulas are combined with conjunction (i.e. all
        subformulas must hold), or otherwise constraining

            z <= sum(z_i)

        if the subformulas are combined with disjuction (at least one
        subformula must hold).
        """
        # We're at the bottom of the tree, so add the big-M constraints
        if isinstance(formula, LinearPredicate):
            # a.T*y - b + (1-z)*M >= rho
            self.model.addConstr( formula.a.T@self.x[:, t] - formula.b + (1-z)*self.M >= self.rho[t] , name=f"STLrho")

            # Force z to be binary
            b = self.model.addMVar(1,vtype=GRB.BINARY)
            self.model.addConstr(z == b)
        
        elif isinstance(formula, NonlinearPredicate):
            raise TypeError("Mixed integer programming does not support nonlinear predicates")

        # We haven't reached the bottom of the tree, so keep adding
        # boolean constraints recursively
        else:
            if formula.combination_type == "and":
                for i, subformula in enumerate(formula.subformula_list):
                    z_sub = self.model.addMVar(1, vtype=GRB.CONTINUOUS)
                    t_sub = formula.timesteps[i]   # the timestep at which this formula
                                                   # should hold
                    self.AddSubformulaConstraints(subformula, z_sub, t+t_sub)
                    self.model.addConstr(z <= z_sub )

            else:  # combination_type == "or":
                z_subs = []
                for i, subformula in enumerate(formula.subformula_list):
                    z_sub = self.model.addMVar(1,vtype=GRB.CONTINUOUS)
                    z_subs.append(z_sub)
                    t_sub = formula.timesteps[i]
                    self.AddSubformulaConstraints(subformula, z_sub, t+t_sub)
                self.model.addConstr( z <= sum(z_subs) )


    def AddQuadraticInputCost(self, R):

        self.cost += self.u[:, 0]@R@self.u[:, 0]
        for t in range(1, self.T):
            self.cost += self.u[:, t]@R@self.u[:, t]

        if self.verbose:
            print(type(self.cost))


    def AddRiskCost(self):
        self.cost += np.ones(self.risk.shape).T @ self.risk


    # Solve the optimization problem
    def Solve(self):
        # Set the cost function now, right before we solve.
        # This is needed since model.setObjective resets the cost.
        self.model.setObjective(self.cost, GRB.MINIMIZE)

        # To prevent gurobi flag message 4
        # self.model.setParam(GRB.Param.DualReductions, 0) # Uncomment

        # Resolve non convexity
        self.model.params.NonConvex = 2

        # Do the actual solving
        self.model.optimize()

        if self.model.status == GRB.OPTIMAL:
            if self.verbose:
                print("\nOptimal Solution Found!\n")
            x = self.x.X
            u = self.u.X
            risk = self.risk.X

            # Report optimal cost and robustness
            if self.verbose:
                print("Solve time: ", self.model.Runtime)
                print("Optimal robustness: ", risk)
                print("")
        else:

            if self.verbose:
                print(f"\nOptimization failed with status {self.model.status}.\n")
            x = None
            u = None
            risk = -np.inf

        return (x, u, risk, self.model.status, self.model.Runtime)
    