# import sys
# sys.path.append(r'E:\_WorkSpace\opstool\src')

import openseespy.opensees as ops
from opstool import load_ops_examples
from opstool.preprocessing import gen_grav_load
from opstool.vis import GetFEMdata, OpsVisPlotly, OpsVisPyvista

load_ops_examples("ArchBridge2")
#load_ops_examples("CableStayedBridge")
# load_ops_examples("Dam")
# load_ops_examples("Frame3D")
# load_ops_examples("Igloo")
# load_ops_examples("Pier")
#load_ops_examples("SuspensionBridge")
# bz.PlotModel(plotmode=6)
# bz.PlotModeShape(plotmode=6, mode_number=1, sacle_factor=100)

ModelData = GetFEMdata()
ModelData.get_model_data()
ModelData.get_eigen_data(mode_tag=15)
opsv = OpsVisPyvista(point_size=2, line_width=2, colors_dict=None, theme="paraview",
                     color_map="coolwarm", on_notebook=False, results_dir="opstool_output")
opsv.model_vis(show_node_label=False, show_ele_label=False,
               show_local_crd=True, label_size=8,
               show_outline=True,
               opacity=1.0, )
opsv.eigen_vis(mode_tags=[1, 15], subplots=False,
               alpha=None, show_outline=False,
               show_origin=False, opacity=1.0,
               show_face_line=True)

# opsv.eigen_anim(mode_tag=4, alpha=None, show_outline=False,
#                 opacity=1, framerate=3,
#                 show_face_line=True,
#                 save_html="EigenAnimation")

# responses
gen_grav_load(ts_tag=1, pattern_tag=1,
              factor=-9.81, direction="Z")
# nodeTags = ops.getNodeTags()
# ops.recorder('Node', '-file', 'Node_displacements.out', '-time', '-node', *nodeTags, '-dof', 1, 2, 3, 'disp')
# import numpy as np
# data = np.loadtxt('Node_displacements.out')
# data[:, 0]
# 分析参数设置
Nsteps = 10  # 分析10步
ops.wipeAnalysis()
ops.system('BandGeneral')
ops.constraints('Transformation')
ops.numberer('RCM')
ops.test('NormDispIncr', 1.0e-12, 10, 3)
ops.algorithm('Linear')
ops.integrator('LoadControl', 1 / Nsteps)
ops.analysis('Static')

ModelData.reset_steps_state()
for i in range(Nsteps):
    a = ops.analyze(1)
    ModelData.get_node_resp_step(num_steps=Nsteps,
                                 model_update=False)
    ModelData.get_frame_resp_step(num_steps=Nsteps)
opsv.deform_vis(slider=True,
                response="disp", alpha=None,
                show_outline=False, show_origin=False,
                show_face_line=False, opacity=1,
                model_update=False)
opsv.deform_anim(
                 # save_fig="yan.gif",
                 response="disp", alpha=None,
                 show_outline=False,
                 show_face_line=False, opacity=1,
                 framerate=3,
                 model_update=False)
opsv.frame_resp_vis(ele_tags=None,
                    slider=True,
                    response="mz",
                    show_values=False,
                    alpha=None,
                    opacity=1)
