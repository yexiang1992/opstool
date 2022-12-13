import os
import openseespy.opensees as ops
from opstool.vis import GetFEMdata, OpsVisPlotly, OpsVisPyvista
from opstool import load_ops_examples

load_ops_examples("DamBreak")
# print(len(ops.getNodeTags('-mesh', 5)))
# print(len(ops.getEleTags()))
# print(ops.eleNodes(5000))
ModelData = GetFEMdata()
ModelData.get_model_data()
# ModelData.get_eigen_data(mode_tag=15)
opsv = OpsVisPyvista(point_size=0.01, line_width=2, colors_dict=None, theme="document",
                     color_map="jet", on_notebook=False, results_dir="opstool_output")
opsv.model_vis(show_node_label=False, show_ele_label=False,
               show_local_crd=False, label_size=8,
               show_outline=True,
               opacity=1.0,)

dtmax = 0.001
dtmin = 1e-6
totaltime = 0.5
alpha = 1.4
b2 = -9.81
# create constraint object
ops.constraints('Plain')

# create numberer object
ops.numberer('Plain')

# create convergence test object
ops.test('PFEM', 1e-5, 1e-5, 1e-5, 1e-5, 1e-15, 1e-15, 20, 3, 1, 2)

# create algorithm object
ops.algorithm('Newton')

# create integrator object
ops.integrator('PFEM')

# create SOE object
ops.system('PFEM')

# create analysis object
ops.analysis('PFEM', dtmax, dtmin, b2)

# analysis
ModelData.reset_steps_state()
while ops.getTime() < totaltime:
    # analysis
    ok = ops.analyze()
    ModelData.get_node_resp_step(analysis_tag=1, total_time=totaltime)
    if ok < 0:
        break
    ops.remesh(alpha)
opsv.deform_vis(analysis_tag=1, slider=True,
                response="disp", alpha=None,
                show_outline=False, show_origin=False,
                show_face_line=True, opacity=1,
                model_update=False)

opsv.deform_anim(analysis_tag=1,
                 save_fig="yan.gif",
                 response="disp", alpha=None,
                 show_outline=False,
                 show_face_line=True, opacity=1,
                 framerate=50,
                 model_update=False)
