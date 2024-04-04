# Risk-Aware Stochastic MPC for Run-Time Specifications in Signal Temporal Logic (RAM-RuTS)

A Python library used to perform Model Predictive Control (MPC) for a single stochastic agent with run-time Signal Temporal Logic specifications.

## Quick Information

This library is used to facilitate the capability of robotic systems to execute dynamically assigned tasks with strict risk limitation.

### Scenario

This library considers an essential case handing scenario as follows, where a robot is required to:

- Start from `HOME`;
- Reach a `TARGET` on request;
- Reach the `CHARGER` on request;
- Visit `HOME` sufficiently often on request;
- Stay inside the work space.

`On request` means that the corresponding tasks are dynamically assigned without prior notice. The robot is required to accomplish these dynamically assigned tasks with a strict safety guarantee in a probability sense.

[![MIT license](map.svg)](CASE)

### Associated Research Work

This library is associated with the Arxiv article in [https://arxiv.org/abs/2402.03165](https://arxiv.org/abs/2402.03165) which is to be presented on the 8th IFAC Conference on Analysis and Design of Hybrid Systems, July 1-3, 2024.


### Relation with Existing Toolbox

The `probstlpy` library in this project is modified from the [stlpy](https://github.com/vincekurtz/stlpy/blob/main/README.md) toolbox. 

## Installation

### System Requirements

**Operating system**
 - *Windows* (compatible in general, successfully tested on 11)
 - *Linux* (compatible in general, successfully tested on 20.04)
 - *MacOS* (compatible in general)

**Python Environment**
 - Python version: test passed on `python=3.11`
 - **Recommended**: IDE ([VS code](https://code.visualstudio.com/) or [Pycharm](https://www.jetbrains.com/pycharm/)) and [Conda](https://www.anaconda.com/)
 - Required Packages: `numpy`, `treelib`, `matplotlib`, `scipy`. 
 
 **Required Libraries**
 - `gurobipy` solver (**license** required, see [How to Get a Gurobi License](https://www.gurobi.com/solutions/licensing/))
 - `Python control` toolbox (see [Documentation](https://python-control.readthedocs.io/en/latest/intro.html))
 
### Quick Installation
 
1. Install conda following this [instruction](https://conda.io/projects/conda/en/latest/user-guide/install/index.html);

2. Open conda shell, create an independent project environment;
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

6. Last but not least, activate the `gurobi` license (See [How To](https://www.gurobi.com/documentation/current/remoteservices/licensing.html)). Note that this project is compatible with `gurobi` Released version `11.0.1`. Keep your `gurobi` updated in case incompatibility. 

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
- Customize the lists of runtime specifications `specs` and their instants `times` for various tasks.

## License

This project is with a BSD-3 license, refer to `LICENSE` for details.
