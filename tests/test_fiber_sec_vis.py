import numpy as np
import openseespy.opensees as ops
from opstool import load_ops_examples
from opstool.vis import GetFEMdata, FiberSecVis


load_ops_examples("SDOF")

FEMdata = GetFEMdata()
FEMdata.get_fiber_data([(1, 1)])
vis = FiberSecVis(ele_tag=1, sec_tag=1, opacity=1, colormap='viridis')
vis.sec_vis(mat_color={1: 'green', 2: 'red', 3: 'black'})

vis.sec_vis()

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
vis.animation(analysis_tag=1,
              output_file='yan.gif',
              show_variable='strain',
              show_mats=[1, 2, 3],
              framerate=10)
