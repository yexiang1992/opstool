import openseespy.opensees as ops
import opstool as opst
ops.wipe()
m = 100/386
ops.model('BasicBuilder', '-ndm', 2, '-ndf', 3)
ops.node(1, 0.0, 0.0)
ops.node(2, 288.0, 0.0)
ops.node(3, 0.0, 144.0)
ops.node(4, 288.0, 144.0)
ops.node(5, 0.0, 288.0)
ops.node(6, 288.0, 288.0)
ops.fix(1, 1, 1, 1)
ops.fix(2, 1, 1, 1)
ops.equalDOF(3, 4, 2, 3)
ops.equalDOF(5, 6, 2, 3)
ops.mass(3, 0.25906735751295334, 0.0, 0.0)
ops.mass(4, 0.25906735751295334, 0.0, 0.0)
ops.mass(5, 0.12953367875647667, 0.0, 0.0)
ops.mass(6, 0.12953367875647667, 0.0, 0.0)
ops.geomTransf('Linear', 1)
ops.element('elasticBeamColumn', 1, 1, 3, 63.41, 30000, 640, 1)
ops.element('elasticBeamColumn', 2, 3, 5, 63.41, 30000, 320, 1)
ops.element('elasticBeamColumn', 3, 2, 4, 63.41, 30000, 640, 1)
ops.element('elasticBeamColumn', 4, 4, 6, 63.41, 30000, 320, 1)
ops.element('elasticBeamColumn', 5, 3, 4, 63.41, 30000, 10000000000000, 1)
ops.element('elasticBeamColumn', 6, 5, 6, 63.41, 30000, 10000000000000, 1)
ops.recorder('Node', '-file', 'modes/mode1.out',
             '-nodeRange', 1, 6, '-dof', 1, 2, 3, 'eigen 1')
ops.recorder('Node', '-file', 'modes/mode2.out',
             '-nodeRange', 1, 6, '-dof', 1, 2, 3, 'eigen 2')
# ops.eigen(2,)
Lambda = ops.eigen('-fullGenLapack', 6)
ModelData = opst.GetFEMdata(results_dir="opstool_output")
ModelData.get_model_data(save_file="ModelData.hdf5")
opsvis = opst.OpsVisPlotly(point_size=2, line_width=3, colors_dict=None, theme="plotly",
                           color_map="jet", on_notebook=True, results_dir="opstool_output")

opsvis.model_vis(input_file="ModelData.hdf5",
                 show_node_label=False,
                 show_ele_label=False,
                 show_local_crd=True,
                 show_fix_node=True,
                 show_constrain_dof=True,
                 label_size=8,
                 show_outline=True,
                 opacity=1.0,
                 save_html='modd')
ModelData.get_eigen_data(mode_tag=4, solver="-fullGenLapack",
                         save_file='EigenData.hdf5')

opsvis.eigen_vis(input_file='EigenData.hdf5',
                 mode_tags=[1, 4], subplots=False,
                 alpha=None, show_outline=False,
                 show_origin=False, opacity=1.0,
                 show_face_line=False, save_html='vvvvvvv')
