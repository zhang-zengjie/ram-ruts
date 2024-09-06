# Risk-Aware Stochastic MPC for Run-Time Specifications in Signal Temporal Logic (RAM-RuTS)

**Author:** Zengjie Zhang (z.zhang3@tue.nl), Maico H.W. Engelaar (m.h.w.engelaar@tue.nl)

A Python library used to perform Model Predictive Control (MPC) for a stochastic linear system with runtime Signal Temporal Logic specifications.

## Introduction

A practical engineering system is often required to accomplish given tasks with restricted risk levels. This can be achieved by risk-aware control incorporating the stochastic uncertainty of the system, rendering a stochastic planning problem with signal temporal logic (STL) specifications. 

Nevertheless, many practical applications need to dynamically assign tasks to the system during runtime. This requires the system to adjust or reschedule its current control strategy to accept the new task. Consider the following restaurant service robot scenario (as illustrated in **Figure 1**), where a service robot staying at the counter (**HOME**) is required to serve two tables (**TARGETS**) while avoiding collision with the wall (**OBSTACLE**). When short of power, it also need to stay in the **CHARGER** for a certain period of time. These tasks may be assigned sequentially in the runtime, some of which are even subject to concurrency or conflict. An example of a task sequence may look like this:

- The robot start from `HOME` at time $0$. It should not go outside the restaurant during the whole time and cannot collide with the wall;
- At time $5$, the robot receives a command "reaching either `TARGET` between time $20$ and $30$";
- At time $15$, the robot receives a command "reaching the `CHARGER` between time $20$ and $25$";
- At time $20$, the robot receives a command "visit `HOME` between $25$ and $30$ and stay there for at least $5$ steps".

In this setting, the robot needs to reschedule its control strategy each time a new dynamic task is assigned. We expect the robot to accomplish the dynamically as many as possible. However, when the robot realize that it has a high risk of conflict or failure, it can reject the new task while fully focusing on the ongoing task. **Figure 1** illustrate a solution where a robot accomplishes all assigned tasks. The blue line is its actual trajectory, implying sequential reaching "**HOME** $\rightarrow$ **CHARGER** $\rightarrow$ **TARGET** $\rightarrow$ **HOME**", while the lines in other colors are contemporarily planned trajectories that have been rescheduled in each stage.

[![Map](map.svg)](CASE)

**Figure 1. a restaurant service robot scenario.**

### Approach

In a risk-aware control framework, we formulate the physical model of the robot as a single-integrator dynamic system with random dynamic noise and use a set of STL to describe the tasks above. In this sense, risk is quantified by the probability that a certain STL task is not satisfied. The risk also serves as an evidence to support the decision-making of the robot whether a new task should be accepted or rejected. The control synthesis is performed using a tube-based shrinking-horizon model predictive control method. For the theoretical details, please refer to our associated Arxiv paper in [https://arxiv.org/abs/2402.03165](https://arxiv.org/abs/2402.03165) which has been presented in the 8th IFAC Conference on Analysis and Design of Hybrid Systems, July 1-3, 2024.


#### Relation with Existing Toolbox

The `probstlpy` library in this project is modified from the [stlpy](https://github.com/vincekurtz/stlpy/blob/main/README.md) toolbox. 

## Installation

### System Requirements

**Operating system**
 - *Windows* (compatible in general, succeed on 11)
 - *Linux* (compatible in general, succeed on 20.04)
 - *MacOS* (compatible in general, succeed on 13.4.1)

**Python Environment**
 - Python version: test passed on `python=3.11`
 - **Recommended**: IDE ([VS code](https://code.visualstudio.com/) or [Pycharm](https://www.jetbrains.com/pycharm/)) and [Conda](https://www.anaconda.com/)
 - Required Packages: `numpy`, `treelib`, `matplotlib`, `scipy`. 
 
 **Required Libraries**
 - `gurobipy` solver (**license** required, see [How to Get a Gurobi License](https://www.gurobi.com/solutions/licensing/))
 - `Python control` toolbox (see [Documentation](https://python-control.readthedocs.io/en/latest/intro.html))
 
### Quick Installation
 
1. Install conda following this [instruction](https://conda.io/projects/conda/en/latest/user-guide/install/index.html);

2. Open the conda shell, and create an independent project environment;
```
conda create --name ram-ruts python=3.11
```

3. In the same shell, activate the created environment
```
conda activate ram-ruts
```

4. In the same shell, within the `ram-ruts` environment, install the dependencies one by one
 ```
conda install -c anaconda numpy
conda install -c conda-forge treelib
conda install -c conda-forge matplotlib
conda install -c anaconda scipy
```

5. In the same shell, within the `ram-ruts` environment, install the libraries
```
python -m pip install gurobipy
pip install control
```

6. Last but not least, activate the `gurobi` license (See [How To](https://www.gurobi.com/documentation/current/remoteservices/licensing.html)). Note that this project is compatible with `gurobi` Released version `11.0.1`. Keep your `gurobi` updated in case of incompatibility. 

### Running Instructions

- Run the main script `main.py`;
- Watch the terminal for runtime information;
- The figures will show up at the end of running; They are also automatically saved in the root directory;
- The figures may impede each other; Drag the figures for a better view;
- Check out the logging file `INFO.log` for the runtime information.

### Fine-Tuning the Code

Feel free to try out the code with different parameter settings in the `commons/configs.py` file.

- Change the coordinates of the regions in the `RG` dictionary to construct a different map;
- Change the color map in the `CM` dictionary for preferred layout;
- Change the standard deviation variable `Sigma` for different noise levels;
- Change the initial position of the robot in `x0`;
- Customize the lists of runtime specifications `specs` and their instants in `times` for various tasks.

## License

This project is with a BSD-3 license, refer to `LICENSE` for details.
