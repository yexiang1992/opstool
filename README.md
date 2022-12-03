<p align="center">
  <a href="https://github.com/yexiang1992/opstool">opstool</a>
  <p align="center">modelling, visualization, post-processing for OpenSeesPy.</p>
</p>

``opstool`` is a useful toolbox package to help ``OpenSeesPy`` *modelling*, *visualization*, *post-processing of results*, etc. The package is still under development and currently mainly supports *visualization*.

To use, install `opstool` from [pypi]([opstool · PyPI](https://pypi.org/project/opstool/)):

```
pip install --upgrade opstool
```

#### Document

This document and the [`tests/`](https://github.com/yexiang1992/opstool/tree/master/tests)
directory contain many small examples. See
[here]() for the full documentation.

#### Vis Module

```python
import openseespy.opensees as ops
from opstool.preprocessing import gen_grav_load
from opstool.vis import GetFEMdata, OpenSeesVis
from opstool import load_ops_examples

load_ops_examples("CableStayedBridge")
```

```python
ModelData = GetFEMdata()
ModelData.get_model_data()
ModelData.get_eigen_data(mode_tag=15)
opsv = OpenSeesVis(point_size=2, line_width=3, colors_dict=None, theme="plotly",
                   color_map="jet", on_notebook=False, results_dir="opstool_output")
opsv.model_vis(show_node_label=False, show_ele_label=False,
               show_local_crd=True, label_size=8,
               show_outline=True,
               opacity=1.0,
               save_html='ModelVis.html')
```

You will get a HTML file geneted by ``plotly``  as fllows:

![CableBridgeModelVis.png](https://s2.loli.net/2022/12/02/iPhmRDaO83AVkbv.png)

You can also display the **eigen analysis**:

<!--pytest-codeblocks:skip-->

```python
opsv.eigen_vis(mode_tags=[1, 9], subplots=True,
               alpha=None, show_outline=False,
               show_origin=False, opacity=1.0,
               show_face_line=False, save_html="EigenVis")
```

![CableBridgeEigenVis.png](https://s2.loli.net/2022/12/02/3UzvQldb8CSIYJw.png)

**Deformation**

```python
# apply gravity load
gen_grav_load(ts_tag=10, pattern_tag=10,
              g=9.81, factor=-1.0, direction="Z")
# analysis set
Nsteps = 10
ops.wipeAnalysis()
ops.system('BandGeneral')
ops.constraints('Transformation')
ops.numberer('RCM')
ops.test('NormDispIncr', 1.0e-12, 10, 3)
ops.algorithm('Linear')
ops.integrator('LoadControl', 1 / Nsteps)
ops.analysis('Static')
# save data
ModelData.reset_steps_state()
for i in range(Nsteps):
    a = ops.analyze(1)
    ModelData.get_node_resp_step(analysis_tag=1,
                                 num_steps=Nsteps,
                                 model_update=False)
    ModelData.get_frame_resp_step(analysis_tag=1, num_steps=Nsteps,)


# display
opsv.deform_vis(analysis_tag=1, slider=True,
                response="disp", alpha=None,
                show_outline=False, show_origin=True,
                show_face_line=False, opacity=1,
                save_html="DefoVis",
                model_update=False)
```

![CableBridgeDefoVis.png](https://s2.loli.net/2022/12/02/qV2XzOkiMQTRl5D.png)

**Frame element forces**

```python
opsv.frame_resp_vis(analysis_tag=1,
                    ele_tags=None,
                    slider=False,
                    response="My",
                    show_values=False,
                    alpha=None,
                    opacity=1,
                    save_html="FrameRespVis")
```

![](https://s2.loli.net/2022/12/02/5rWeYB6Uw4Si31d.png)

#### Fiber section vis

```python
import numpy as np
import openseespy.opensees as ops
from opstool import load_ops_examples
from opstool.vis import GetFEMdata, FiberSecVis


load_ops_examples("SDOF")

FEMdata = GetFEMdata()
FEMdata.get_fiber_data([(1, 1)])
vis = FiberSecVis(ele_tag=1, sec_tag=1, opacity=1, colormap='viridis')
vis.sec_vis(mat_color={1: 'gray', 2: 'orange', 3: 'black'})

```

![FiberSecVis.png](https://s2.loli.net/2022/12/03/jwvVecT3GCWbdBI.png)

```python
# --------------------------------------------------
# dynamic load
ops.rayleigh(0.0, 0.0, 0.0, 0.000625)
ops.loadConst('-time', 0.0)

# applying Dynamic Ground motion analysis
dt = 0.02
ttot = 5
npts = int(ttot / dt)
x = np.linspace(0, ttot, npts)
data = np.sin(2 * np.pi * x)
ops.timeSeries('Path', 2, '-dt', dt, '-values', *data, '-factor', 9.81)
# how to give accelseriesTag?
ops.pattern('UniformExcitation', 2, 1, '-accel', 2)
# how to give accelseriesTag?
ops.pattern('UniformExcitation', 3, 2, '-accel', 2)

ops.wipeAnalysis()
ops.system('BandGeneral')
# Create the constraint handler, the transformation method
ops.constraints('Transformation')
# Create the DOF numberer, the reverse Cuthill-McKee algorithm
ops.numberer('RCM')
ops.test('NormDispIncr', 1e-8, 10)
ops.algorithm('Linear')
ops.integrator('Newmark', 0.5, 0.25)
ops.analysis('Transient')

for i in range(npts):
    ops.analyze(1, dt)
    FEMdata.get_fiber_resp_step(analysis_tag=1, num_steps=npts)

vis.resp_vis(analysis_tag=1, step=None,
             show_variable='strain',
             show_mats=[1, 2, 3],)
```

![FiberSecVis2.png](https://s2.loli.net/2022/12/03/NQ5VOA6iUFtY9af.png)

#### Section Mesh

```python
import numpy as np
from opstool.preprocessing import SecMesh, add_material, add_polygon, add_circle, offset, Rebars
```

```python
# Case 5
outlines = [[0.5, 0], [7.5, 0], [8, 0.5], [8, 4.5],
            [7.5, 5], [0.5, 5], [0, 4.5], [0, 0.5]]
cover_d = 0.08
coverlines = offset(outlines, d=cover_d)
cover = add_polygon(outlines, holes=[coverlines])
holelines1 = [[1, 1], [3.5, 1], [3.5, 4], [1, 4]]
holelines2 = [[4.5, 1], [7, 1], [7, 4], [4.5, 4]]
core = add_polygon(coverlines, holes=[holelines1, holelines2])
sec = SecMesh()
sec.assign_group(dict(cover=cover, core=core))
sec.assign_mesh_size(dict(cover=0.2, core=0.4))
sec.assign_group_color(dict(cover="gray", core="green"))
sec.assign_ops_matTag(dict(cover=1, core=2))
sec.mesh()
# add rebars
rebars = Rebars()
rebar_lines1 = offset(outlines, d=cover_d + 0.032 / 2)
rebars.add_rebar_line(
    points=rebar_lines1, dia=0.032, gap=0.15, color="red", matTag=3
)
rebar_lines2 = offset(holelines1, d=-(0.05 + 0.02 / 2))
rebars.add_rebar_line(
    points=rebar_lines2, dia=0.020, gap=0.2, color="black", matTag=3
)
rebar_lines3 = offset(holelines2, d=-(0.05 + 0.02 / 2))
rebars.add_rebar_line(
    points=rebar_lines3, dia=0.020, gap=0.2, color="black", matTag=3
)
# add to the sec
sec.add_rebars(rebars)
sec_props = sec.get_sec_props(display_results=True, plot_centroids=False)
sec.centring()
# sec.rotate(45)
sec.view(fill=True, engine='plotly', save_html="SecMesh.html")
G = 10000
sec.to_file("mysec.py", secTag=1, GJ=G * sec_props['J'])

```

![SecMesh.png](https://s2.loli.net/2022/12/03/Jla3yTh1QxVZ9pk.png) 

### License

This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).
