[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

# Risk-Aware MPC for Run-Time Temporal Logic (RaM-RutTL)

A Python library used to perform Model Predictive Control (MPC) for a single stochastic agent with Run-Time Temporal Logic

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

Feel free to try out the code with different parameter settings in the `configs.py' file.

- Change the rectangular regions `WORKSPACE', `HOME', `TARGETA', `TARGETB'

## License

For the license of this library, refer to `LICENSE`.
