import numpy as np
import openseespy.opensees as ops
import opstool as opst

#
opst.load_ops_examples("SDOF")

FEMdata = opst.GetFEMdata()
FEMdata.get_fiber_data([(1, 1)])
vis = opst.FiberSecVis(ele_tag=1, sec_tag=1, opacity=1, colormap='viridis')
vis.sec_vis(mat_color={1: 'gray', 2: 'orange', 3: 'black'})

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
# ops.test('NormDispIncr', 1e-8, 10)
# ops.algorithm('Linear')
ops.integrator('Newmark', 0.5, 0.25)
ops.analysis('Transient')

analysis = opst.SmartAnalyze(analysis_type="Transient",
                             debugMode=True)
segs = analysis.transient_split(npts)
for i in range(npts):
    lucky = analysis.TransientAnalyze(dt)
    FEMdata.get_fiber_resp_step(num_steps=npts)

vis.resp_vis(step=None,
             show_variable='strain',
             show_mats=[1, 2, 3],)
vis.animation(
    output_file='yan.gif',
    show_variable='strain',
    show_mats=[1, 2, 3],
    framerate=10)
