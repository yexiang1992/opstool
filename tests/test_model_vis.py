# import sys
# sys.path.append(r'E:\_WorkSpace\opstool\src')
#%%
import openseespy.opensees as ops
import opstool as opst

#
# opst.load_ops_examples("ArchBridge")
opst.load_ops_examples("CableStayedBridge")
# opst.load_ops_examples("Dam")
# opst.load_ops_examples("Frame3D")
# load_ops_examples("Igloo")
# load_ops_examples("Pier")
# opst.load_ops_examples("SuspensionBridge")
# bz.PlotModel(plotmode=6)
# bz.PlotModeShape(plotmode=6, mode_number=1, sacle_factor=100)
opst.plot_model(backend="pyvista")    # or backend="plotly"
opst.plot_eigen(mode_tags=[1, 12], backend="pyvista", subplots=True)   # or backend="plotly"

ModelData = opst.GetFEMdata()
ModelData.get_model_data()
ModelData.get_eigen_data(mode_tag=15)
opsv = opst.OpsVisPlotly(point_size=2, line_width=2, colors_dict=None, theme="plotly",
                     color_map="jet", on_notebook=False, results_dir="opstool_output")
opsv.model_vis(show_node_label=False, show_ele_label=False,
               show_local_crd=False, show_fix_node=True, label_size=8,
               show_outline=False,
               opacity=1.0)

# #%%
# opst.save_tikz("opstool_output/ModelData.hdf5")
# opsv.eigen_vis(mode_tags=[1, 12], subplots=True,
#                alpha=None, show_outline=False,
#                show_origin=False, opacity=1.0,
#                show_face_line=False,)

# opsv.eigen_anim(mode_tag=4, alpha=None, show_outline=False,
#                 opacity=1, framerate=3,
#                 show_face_line=True)

# # responses
# opst.gen_grav_load(ts_tag=1, pattern_tag=1,
#               factor=-9.81, direction="Z")
# # nodeTags = ops.getNodeTags()
# # ops.recorder('Node', '-file', 'Node_displacements.out', '-time', '-node', *nodeTags, '-dof', 1, 2, 3, 'disp')
# # import numpy as np
# # data = np.loadtxt('Node_displacements.out')
# # data[:, 0]
# # 分析参数设置
# Nsteps = 10  # 分析10步
# ops.wipeAnalysis()
# ops.system('BandGeneral')
# ops.constraints('Transformation')
# ops.numberer('RCM')
# ops.test('NormDispIncr', 1.0e-12, 10, 3)
# ops.algorithm('Linear')
# ops.integrator('LoadControl', 1 / Nsteps)
# ops.analysis('Static')

# for i in range(Nsteps):
#     a = ops.analyze(1)
#     ModelData.get_resp_step()
# ModelData.save_resp_all(save_file="RespStepData-1.hdf5")
# opsv.deform_vis(input_file="RespStepData-1.hdf5",
#                 slider=True,
#                 response="disp", alpha=None,
#                 show_outline=False, show_origin=False,
#                 show_face_line=False, opacity=1,
#                 model_update=False)
# #%%
# # opsv.deform_anim(input_file="RespStepData-1.hdf5",
# #                  # save_fig="yan.gif",
# #                  response="disp", alpha=None,
# #                  show_outline=False,
# #                  show_face_line=False, opacity=1,
# #                  framerate=3,
# #                  model_update=False)
# opsv.react_vis(input_file="RespStepData-1.hdf5",
#                slider=True,
#                direction="Fz")
# opsv.frame_resp_vis(input_file="RespStepData-1.hdf5",
#                     ele_tags=None,
#                     slider=True,
#                     response="my",
#                     show_values=False,
#                     alpha=None,
#                     opacity=1)

# %%
