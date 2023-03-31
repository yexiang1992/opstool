<p align="center">
  <font size=7><a href="https://github.com/yexiang1992/opstool">opstool</a></font>
  <p align="center"><font size=5 color=YellowGreen>modelling, visualization, post-processing for OpenSeesPy.</font></p>
</p>

[![pypi](https://img.shields.io/pypi/v/opstool)](https://pypi.org/project/opstool/)
[![Downloads](https://static.pepy.tech/badge/opstool)](https://pepy.tech/project/opstool)
[![Documentation Status](https://readthedocs.org/projects/opstool/badge/?version=latest)](https://opstool.readthedocs.io/en/latest/?badge=latest)
[![github stars](https://img.shields.io/github/stars/yexiang1992/opstool?style=social)](https://github.com/yexiang1992/opstool)
![license](https://img.shields.io/github/license/yexiang1992/opstool)
[![code grade](https://img.shields.io/codefactor/grade/github/yexiang1992/opstool)](https://www.codefactor.io/repository/github/yexiang1992/opstool)

`opstool` is a useful toolbox package aims to help [OpenSeesPy](https://openseespydoc.readthedocs.io/en/latest/) _pre-processing_, _visualization_, _analysis-aid_, etc.
The package is still under development.

To use, install `opstool` from [opstool-PyPI](https://pypi.org/project/opstool/):

```python
pip install --upgrade opstool
```

The restriction on the python version mainly depends on `openseespy`,
it is recommended that you use [Anaconda](https://www.anaconda.com/) to avoid library version incompatibilities.

### Document

**Latest**: See [https://opstool.readthedocs.io/en/latest/](https://opstool.readthedocs.io/en/latest/).

**Stable**: See [https://opstool.readthedocs.io/en/stable/](https://opstool.readthedocs.io/en/stable/)

### Visualization

#### Based on [plotly](https://plotly.com/python/)

|                          Model                          |                          Modal                          |                       Deformation                       |
| :-----------------------------------------------------: | :-----------------------------------------------------: | :-----------------------------------------------------: |
| ![](https://s2.loli.net/2023/03/27/CvGfgAi6IMlw9JQ.png) | ![](https://s2.loli.net/2023/03/27/r1NaUGuiEcjJMYn.png) | ![](https://s2.loli.net/2023/03/27/TzL3YsmPQU1nlx8.png) |
| ![](https://s2.loli.net/2023/03/27/cUXb3oJF6BuqpCg.png) | ![](https://s2.loli.net/2023/03/27/LstpljZ6SWqJCzU.png) | ![](https://s2.loli.net/2023/03/27/ejBhzgDwR4NAcdM.png) |
| ![](https://s2.loli.net/2023/03/27/hSYqerWg9O5xmvB.png) | ![](https://s2.loli.net/2023/03/27/MWqZnDu8hUF4wBt.png) | ![](https://s2.loli.net/2023/03/27/1yVpOlzWgHGLBRC.png) |

<!-- ![CableBridgeModelVis.png](https://s2.loli.net/2022/12/02/iPhmRDaO83AVkbv.png)

![CableBridgeEigenVis.png](https://s2.loli.net/2022/12/02/3UzvQldb8CSIYJw.png)

![CableBridgeDefoVis.png](https://s2.loli.net/2022/12/02/qV2XzOkiMQTRl5D.png) -->

#### Based on [pyvista](https://docs.pyvista.org/)

|                          Model                          |                          Eigen                          |                       Deformation                       |
| :-----------------------------------------------------: | :-----------------------------------------------------: | :-----------------------------------------------------: |
| ![](https://s2.loli.net/2023/03/27/NfVY135ibDSdCgj.png) | ![](https://s2.loli.net/2023/03/27/r1NaUGuiEcjJMYn.png) | ![](https://s2.loli.net/2023/03/27/EMo5lJx2eC9zSm4.png) |
| ![](https://s2.loli.net/2023/03/27/YWVnahNiwgFS6tE.png) | ![](https://s2.loli.net/2023/03/27/vFuV8IfHosRJYkG.png) | ![](https://s2.loli.net/2023/03/27/KFzs3qoy2cEWl7u.png) |
| ![](https://s2.loli.net/2023/03/27/fPgMBHSrNJazbCI.png) | ![](https://s2.loli.net/2023/03/27/Ei9tMheJm5LPuax.png) | ![](https://s2.loli.net/2023/03/27/xE1CycfZYhTW6OX.png) |

<!-- ![None.png](https://s2.loli.net/2022/12/07/TElXvIoDZFAfysc.png)

![None.png](https://s2.loli.net/2022/12/07/bMqL2kKHpN4XBeZ.png) -->

#### Animation

|                          Eigen                          |                       Deformation                       |
| :-----------------------------------------------------: | :-----------------------------------------------------: |
| ![](https://s2.loli.net/2022/12/07/akOEebwrNZCuj2V.gif) | ![](https://s2.loli.net/2022/12/07/KVEYO6eC8hlWvXg.gif) |

#### Fiber section vis

|                        &#x2705;                         |                        &#x2705;                         |
| :-----------------------------------------------------: | :-----------------------------------------------------: |
| ![](https://s2.loli.net/2022/12/03/jwvVecT3GCWbdBI.png) | ![](https://s2.loli.net/2022/12/03/NQ5VOA6iUFtY9af.png) |

### Fiber Section Mesh Generation

|                        &#x2705;                         |                        &#x2705;                         |                        &#x2705;                         |
| :-----------------------------------------------------: | :-----------------------------------------------------: | :-----------------------------------------------------: |
| ![](https://s2.loli.net/2023/03/27/bRYlfP8vNLEeJxF.png) | ![](https://s2.loli.net/2023/03/27/XfPkFKYmZEWJqnc.png) | ![](https://s2.loli.net/2023/03/27/YuwXlkZCIQRnsiK.png) |
| ![](https://s2.loli.net/2023/03/27/z2JvO3B9GD8EnkC.png) | ![](https://s2.loli.net/2023/03/27/ci3DtqojAy9zfeH.png) | ![](https://s2.loli.net/2023/03/27/Ss3rlzUv7u2Pjp6.png) |

### Moment-Curvature Analysis of Fiber Section

|                      Section Mesh                       |                Moment-Curvature Analysis                |
| :-----------------------------------------------------: | :-----------------------------------------------------: |
| ![](https://s2.loli.net/2023/03/27/z6S4sL8RbfeApV7.png) | ![](https://s2.loli.net/2023/03/27/lGFdgMypkxHW3PU.png) |

### License

This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).
