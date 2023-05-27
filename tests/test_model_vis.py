# %%
import openseespy.opensees as ops
import opstool as opst

#
opst.load_ops_examples("ArchBridge")
# opst.load_ops_examples("CableStayedBridge")
# opst.load_ops_examples("Dam")
# opst.load_ops_examples("Frame3D")
# opst.load_ops_examples("Igloo")
# opst.load_ops_examples("Pier")
# opst.load_ops_examples("SuspensionBridge")
# opst.plot_model(backend="pyvista")    # or backend="plotly"
# opst.plot_eigen(mode_tags=[1, 12], backend="pyvista", subplots=True)   # or backend="plotly"
# opst.gen_grav_load(ts_tag=1, pattern_tag=1, factor=-9.81, direction="Z")
ModelData = opst.GetFEMdata()
ModelData.get_model_data()
ModelData.get_eigen_data(mode_tag=15)
opsv = opst.OpsVisPlotly(
    point_size=4,
    line_width=4,
    colors_dict=None,
    color_map="jet",
    on_notebook=False,
    results_dir="opstool_output",
)
fig = opsv.model_vis(
    show_node_label=False,
    show_ele_label=False,
    show_local_crd=False,
    show_fix_node=True,
    # show_load=True,
    # load_alpha=0.5,
    label_size=8,
    show_outline=True,
    opacity=1.0,
)
fig.show()
# fig.write_html("ModelVis.html", auto_open=True)
# %%
opst.save_tikz("opstool_output/ModelData.hdf5")
opsv.eigen_vis(
    mode_tags=[1, 12],
    subplots=True,
    alpha=1.0,
    show_outline=False,
    show_origin=False,
    opacity=1.0,
    show_face_line=False,
)

opsv.eigen_anim(
    mode_tag=4,
    alpha=1.0,
    show_outline=False,
    opacity=1,
    framerate=3,
    show_face_line=True,
    save_fig="1.mp4",
)

# responses
opst.gen_grav_load(ts_tag=1, pattern_tag=1, factor=-9.81, direction="Z")
# nodeTags = ops.getNodeTags()
# ops.recorder('Node', '-file', 'Node_displacements.out', '-node', *nodeTags, '-dof', 1, 2, 3,4,5,6, 'disp')
# import numpy as np
# data = np.loadtxt('Node_displacements.out')
# data[:, 0]
#
Nsteps = 10
ops.wipeAnalysis()
ops.system("BandGeneral")
ops.constraints("Transformation")
ops.numberer("RCM")
ops.test("NormDispIncr", 1.0e-12, 10, 3)
ops.algorithm("Linear")
ops.integrator("LoadControl", 1 / Nsteps)
ops.analysis("Static")

for i in range(Nsteps):
    a = ops.analyze(1)
    ModelData.get_resp_step()
ModelData.save_resp_all(save_file="RespStepData-1.hdf5")
opsv.deform_vis(
    input_file="RespStepData-1.hdf5",
    slider=True,
    response="disp",
    alpha=1.0,
    show_outline=False,
    show_origin=False,
    show_face_line=False,
    opacity=1,
    model_update=False,
)
# %%
opsv.deform_anim(
    input_file="RespStepData-1.hdf5",
    # save_fig="yan.gif",
    response="disp",
    alpha=1.0,
    show_outline=False,
    show_face_line=False,
    opacity=1,
    framerate=3,
    model_update=False,
)
opsv.react_vis(input_file="RespStepData-1.hdf5", slider=True, direction="Fz")
opsv.frame_resp_vis(
    input_file="RespStepData-1.hdf5",
    ele_tags=None,
    slider=True,
    response="my",
    show_values=False,
    alpha=1.0,
    opacity=1,
)
