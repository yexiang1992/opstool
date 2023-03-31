import opstool as opst
import openseespy.opensees as ops

ops.wipe()
ops.model('basic', '-ndm', 3, '-ndf', 6)

# materials
Ec = 3.55E+7
Vc = 0.2
Gc = 0.5 * Ec / (1 + Vc)
fc = -32.4E+3
ec = -2000.0E-6
ecu = 2.1 * ec
ft = 2.64E+3
et = 107E-6
fccore = -40.6e+3
eccore = -4079e-6
ecucore = -0.0144

Fys = 400.E+3
Fus = 530.E+3
Es = 2.0E+8
eps_sh = 0.0074
eps_ult = 0.095
Esh = (Fus - Fys) / (eps_ult - eps_sh)
bs = 0.01

matTagC = 1
matTagCCore = 2
matTagS = 3
ops.uniaxialMaterial('Concrete04', matTagC, fc, ec, ecu, Ec, ft, et)
ops.uniaxialMaterial('Concrete04', matTagCCore, fccore,
                     eccore, ecucore, Ec, ft, et)  # for core
ops.uniaxialMaterial('ReinforcingSteel', matTagS, Fys,
                     Fus, Es, Esh, eps_sh, eps_ult)

outlines = [[0, 0], [2, 0], [2, 2], [0, 2]]
coverlines = opst.offset(outlines, d=0.05)
cover = opst.add_polygon(outlines, holes=[coverlines])
holelines = [[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]]
core = opst.add_polygon(coverlines, holes=[holelines])
sec = opst.SecMesh()
sec.assign_group(dict(cover=cover, core=core))
sec.assign_mesh_size(dict(cover=0.02, core=0.05))
sec.assign_group_color(dict(cover="gray", core="green"))
sec.assign_ops_matTag(dict(cover=matTagC, core=matTagCCore))
sec.mesh()
# add rebars
rebars = opst.Rebars()
rebar_lines1 = opst.offset(outlines, d=0.05 + 0.032 / 2)
rebars.add_rebar_line(
    points=rebar_lines1, dia=0.02, gap=0.1, color="red",
    matTag=matTagS,
)
sec.add_rebars(rebars)
# sec.get_sec_props(display_results=False, plot_centroids=False)
sec.centring()
# sec.rotate(45)
sec.view(fill=True, engine='matplotlib', save_html=None, on_notebook=True)
# generate the OpenSeesPy commands
sec.opspy_cmds(secTag=1, GJ=100000)
# M-Phi analysis
mc = opst.MomentCurvature(sec_tag=1, axial_force=-10000)
mc.analyze(axis='z')
mc.plot_M_phi()
mc.plot_fiber_responses()
phiy, My = mc.get_limit_state(matTag=matTagS,
                              threshold=2e-3,)
phiu, Mu = mc.get_limit_state(matTag=matTagCCore,
                              threshold=-0.0144,
                              use_peak_drop20=False
                              )
phi_eq, M_eq = mc.bilinearize(phiy, My, phiu, plot=True)
