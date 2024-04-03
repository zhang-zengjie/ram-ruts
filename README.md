[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

# Risk-Aware MPC for Run-Time Temporal Logic (RaM-RutTL)

A Python library used to perform Model Predictive Control (MPC) for a single stochastic agent with Run-Time Temporal Logic

## Installation

### System Requirements

**Operating system**
 - Windows (compatible in general, successfully tested on 11)
 - Linux (compatible in general, successfully tested on 20.04)
 - MacOS (compatible in general)

**Python Environment**
 - Python version: `>=3.7` or `<=3.11`
 - Required Packages: `numpy`, `treelib`, `gurobi`, `matplotlib`, `scipy`. For `conda`, they can be installed using the following commands:
```
conda install -c anaconda numpy
conda install -c conda-forge treelib
conda install -c gurobi gurobi
conda install -c conda-forge matplotlib
conda install -c anaconda scipy
```

**Toolbox stlpy**
This benchmark is based on the [stlpy](https://github.com/vincekurtz/stlpy/blob/main/README.md) toolbox. Please cite the source when you develop your own benchmark.

### Instructions for the single-agent case

- Run `single.main.py` for the single-agent case;
- Run `single.plot.py` to plot the results for the single-agent case;
- Checkout the logging information in `single.info.log`.

### Instructions for the multi-agent case

- Run `auction.main.py` for the multi-agent auction case;
- Run `auction.plot.py` to plot the results for the multi-agent auction case;
- Checkout the logging information in `auction.info.log`.

### License

For the license of the `stlpy` toolbox, refer to `stlpy/LICENSE`.

## Changes made to include multiple rho variables

- Change the dimension of rho variables:
```
self.rho = self.model.addMVar((self.T, ), name="rho", lb=0.0)   # 1->self.T to incorporate multiple dimensions
```
- Change the cost function:
```
def AddRobustnessCost(self):
        self.cost -= np.ones(self.rho.shape).T @ self.rho  # The cost is the negative summary of multiple rho values
```
- Multiple constraints to restrict the limits for rhos
```
def AddRobustnessConstraint(self, rho_min=0.0):
        for rho in self.rho:
            self.model.addConstr( rho >= rho_min )
```
- Multiple constraints to specify the satisfaction of specifications
```
if isinstance(formula, LinearPredicate):
            # self.rho -> self.rho[t]
            self.model.addConstr( formula.a.T@self.y[:,t] - formula.b + (1-z)*self.M  >= self.rho[t] )
```
