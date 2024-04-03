[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

# Risk-Aware MPC for Run-Time Temporal Logic (RaM-RutTL)

A Python library used to perform Model Predictive Control (MPC) for a single stochastic agent with Run-Time Temporal Logic.

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

This library is associated with the Arxiv article in [https://arxiv.org/abs/2402.03165](https://arxiv.org/abs/2402.03165).

## Installation

### System Requirements

**Operating system**
 - *Windows* (compatible in general, successfully tested on 11)
 - *Linux* (compatible in general, successfully tested on 20.04)
 - *MacOS* (compatible in general)

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

### Running Instructions

- Run the main script `main.py` to generate data in `/data`;
- Watch the terminal or check the logging file `/data/INFO.log` for the runtime information;
- Run `plot.py` to plot the results; the figures may impede each other; drag the figures for a better view.

### Fine-Tuning the Code

Feel free to try out the code with different parameter settings in the `configs.py` file.

- Change the coordinates of the regions in the `RG` dictionary to construct a different map;
- Change the color map in the `CM` dictionary for preferred layout;
- Change the standard deviation variable `Sigma` for different noise levels;
- Change the initial position of the robot in `x0`;
- Customize the lists of runtime specifications `specs` and their instants `times` for various tasks.

## License

For the license of this library, refer to `LICENSE`.
