import numpy as np
import openseespy.opensees as ops


ops.wipe()
ops.model('basic', '-ndm', 3, '-ndf', 6)


vc = 0.2
fc = -20.1E3
ec = -2E-3
fcu = -16.5E3
ecu = -4E-3
Ec = 2 * fc / ec
Gc = Ec / (2 * (1 + vc))

# ft40 = 2.39E+3
# et40 = 100.E-6
fccore = -26.8E3
eccore = -5.3E-3
fcucore = -23
ecucore = -0.0157

Fys = 300E3
Es = 2.0E8
bs = 0.01
matTagC = 1
matTagCCore = 2
matTagSteel = 3
ops.uniaxialMaterial('Concrete01', matTagC, fc, ec, fcu, ecu)
ops.uniaxialMaterial('Concrete01', matTagCCore,
                     fccore, eccore, fcucore, ecucore)
ops.uniaxialMaterial('Steel01', matTagSteel, Fys, Es, bs)

ops.node(1, 0.0, 0.0, 0.0)
ops.node(2, 0.0, 0.0, 8.0)
ops.mass(2, 100, 100, 100, 0, 0, 0)
ops.fix(1, 1, 1, 1, 1, 1, 1)

pier_d = 1.3
cover = 0.05
bar_d = 0.022
bar_ratio = 0.01
mesh_size = 0.1

pier_area = np.pi * (pier_d / 2) ** 2
bar_area = np.pi * bar_d * bar_d / 4
bar_num = int(pier_area * bar_ratio / bar_area)
sec_Tag = 1
ops.section('Fiber', sec_Tag, '-GJ', 0.5 * np.pi * (pier_d / 2) ** 4)
ops.patch('circ', matTagC, int(np.pi * pier_d / mesh_size), 1, *
          [0, 0], *[pier_d / 2 - cover, pier_d / 2], *[0, 360])
ops.patch('circ', matTagCCore, int(np.pi * pier_d / mesh_size), int(0.5 * pier_d / mesh_size),
          *[0, 0], *[0, pier_d / 2 - cover], *[0, 360])
ops.layer('circ', matTagSteel, bar_num, bar_area, *[0, 0],
          pier_d / 2 - cover - bar_d / 2, *[0.0, 360.0 - 360 / 35])

ops.geomTransf('Linear', 1, *[-1, 0, 0])
ops.beamIntegration('Lobatto', 1, 1, 6)
ops.element('forceBeamColumn', 1, *[1, 2], 1, 1)
