# opstool
*Pre-Processing, Post-Processing, and Visualization Tailored for OpenSeesPy*

[![pypi](https://img.shields.io/pypi/v/opstool)](https://pypi.org/project/opstool/)
[![Downloads](https://static.pepy.tech/badge/opstool)](https://pepy.tech/project/opstool)
[![Documentation Status](https://readthedocs.org/projects/opstool/badge/?version=latest)](https://opstool.readthedocs.io/en/latest/?badge=latest)
[![github stars](https://img.shields.io/github/stars/yexiang1992/opstool?style=social)](https://github.com/yexiang1992/opstool)
[![GitHub License](https://img.shields.io/github/license/yexiang1992/opstool?style=flat)](https://img.shields.io/github/license/yexiang1992/opstool?style=flat)
[![code grade](https://img.shields.io/codefactor/grade/github/yexiang1992/opstool)](https://www.codefactor.io/repository/github/yexiang1992/opstool)

``opstool`` is a powerful and user-friendly package designed to simplify and enhance structural analysis workflows 
with [OpenSees](https://opensees.berkeley.edu/) and [OpenSeesPy](https://openseespydoc.readthedocs.io/en/latest/). 
It provides advanced tools for preprocessing, postprocessing, and visualization, making structural 
simulations more efficient and accessible.

The package is still under development.
To use, install `opstool` from [opstool-PyPI](https://pypi.org/project/opstool/):

```bash
pip install --upgrade opstool
```

The restriction on the python version mainly depends on `openseespy`,
it is recommended that you use [Anaconda](https://www.anaconda.com/) to avoid library version incompatibilities.

## Document

**Latest**: See [https://opstool.readthedocs.io/en/latest/](https://opstool.readthedocs.io/en/latest/).

**Stable**: See [https://opstool.readthedocs.io/en/stable/](https://opstool.readthedocs.io/en/stable/)

> [!TIP]
> Since an opstool version **v1.0.1**, the API and features have undergone significant changes and upgrades. As a result, it feels more like a new library, and you should take some time to familiarize yourself with the new interface usage.

## Key Features

1. **Preprocessing Tools**:
   - *Fiber Section Meshing*: Generate detailed fiber meshes for various geometries.
      | ![image.png](https://s2.loli.net/2025/02/09/lXGLVFKmIcSsvgN.png) | ![image.png](https://s2.loli.net/2025/02/09/nIxAhN8rLBEQi2t.png) |
   - *GMSH Integration*: Import and convert [Gmsh](https://gmsh.info/) models, including geometry, mesh, and physical groups.
   - *Unit System Management*: Ensure consistency with automatic unit conversions.
   - *Mass Generation*: Automate lumped mass calculations.
2. **Postprocessing Capabilities**:
   - Easy retrieval and interpretation of analysis results using [xarray](https://docs.xarray.dev/en/stable/index.html#).
3. **Visualization**:
   - Powered by [Pyvista](https://docs.pyvista.org/) (VTK-based) and [Plotly](https://plotly.com/python/) (web-based).
   - Nearly identical APIs for flexible visualization of model geometry, modal analysis, and simulation results.
   - Supports most common OpenSees elements.
4. **Intelligent Analysis**:
   - Features like automatic step size adjustment and algorithm switching to optimize simulation workflows.
   - Moment-Curvature Analysis: Generate moment-curvature curves for various sections.

## Why Choose opstool?

- **Efficiency**: Streamlines complex workflows, reducing time spent on repetitive tasks.
- **Flexibility**: Provides nearly identical interfaces for different visualization engines.
- **Accessibility**: Makes advanced structural analysis tools like OpenSeesPy more approachable to users of all levels.

``opstool`` is actively evolving, with continuous additions of new features planned for the future.
With ``opstool``, you can focus on what matters most: 
understanding and solving your structural engineering challenges. 
Whether you are building models, visualizing results, or interpreting data, 
``opstool`` is your go-to solution for OpenSeesPy workflows.

## License

This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).
