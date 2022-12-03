import openseespy.opensees as ops
from opstool.preprocessing import gen_grav_load
from opstool.vis import GetFEMdata, OpenSeesVis
from opstool import load_ops_examples


# load_ops_examples("ArchBridge")
# load_ops_examples("CableStayedBridge")
# load_ops_examples("Dam")
load_ops_examples("Frame3D")
# load_ops_examples("Igloo")
# load_ops_examples("Pier")
# load_ops_examples("SuspensionBridge")

ModelData = GetFEMdata()
ModelData.get_model_data()
ModelData.get_eigen_data(mode_tag=15)
opsv = OpenSeesVis(point_size=2, line_width=3, colors_dict=None, theme="plotly",
                   color_map="jet", on_notebook=False, results_dir="opstool_output")
# opsv.model_vis(show_node_label=False, show_ele_label=False,
#                show_local_crd=True, label_size=8,
#                show_outline=True,
#                opacity=1.0,
#                save_html='ModelVis.html')
# opsv.eigen_vis(mode_tags=[1, 9], subplots=False,
#                alpha=None, show_outline=False,
#                show_origin=False, opacity=1.0,
#                show_face_line=False, save_html="EigenVis")
# opsv.eigen_anim(mode_tag=1, alpha=None, show_outline=True,
#                 opacity=1, framerate=3,
#                 show_face_line=True,
#                 save_html="EigenAnimation")

# responses
gen_grav_load(ts_tag=10, pattern_tag=10,
              g=9.81, factor=-1.0, direction="Z")
# 分析参数设置
Nsteps = 10   # 分析10步
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
    ModelData.get_node_resp_step(analysis_tag=1,
                                 num_steps=Nsteps,
                                 model_update=False)
    ModelData.get_frame_resp_step(analysis_tag=1, num_steps=Nsteps,)
# opsv.deform_vis(analysis_tag=1, slider=False,
#                 response="disp", alpha=None,
#                 show_outline=False, show_origin=True,
#                 show_face_line=False, opacity=1,
#                 save_html="DefoVis",
#                 model_update=False)
# # opsv.deform_anim(analysis_tag=1,
# #                  response="disp", alpha=None,
# #                  show_outline=False,
# #                  show_face_line=False, opacity=1,
# #                  save_html="DefoAnimation",
# #                  model_update=False)
opsv.frame_resp_vis(analysis_tag=1,
                    ele_tags=None,
                    slider=True,
                    response="Mz",
                    show_values=False,
                    alpha=None,
                    opacity=0.5,
                    save_html="FrameRespVis")
