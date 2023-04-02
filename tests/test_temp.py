from openseespy.opensees import *
import opsvis as opsv
import numpy as np
import matplotlib.pyplot as plt
from math import asin, sqrt
import math as mm
import opstool as opst
# Two dimensional Frame: Eigenvalue & Static Loads


# REFERENCES:
# used in verification by SAP2000:
# SAP2000 Integrated Finite Element Analysis and Design of Structures, Verification Manual,
# Computers and Structures, 1997. Example 1.
# and seismo-struct (Example 10)
# SeismoStruct, Verification Report For Version 6, 2012. Example 11.


# set some properties
wipe()

model('Basic', '-ndm', 2, '-ndf', 3)

# properties

#    units kip, ft

numBay = 5
numFloor = 40

bayWidth = 6
storyHeights = 3*np.ones((1,41))

nodeTag=1
yLoc=0
# nDMaterial('PressureIndependMultiYield', 100, 2, 0., 61250., 180000., 35., 0.1)
#多屈服面材料设置有误
# nDMaterial('ElasticIsotropic',100,61250.,0.3)
# t=1.0
# eleArgs = [t,'PlaneStrain',100]
# block2D(10,5,40,57,'quad',*eleArgs, *points)
# # timeSeries("Linear", 1)
# opsv.plot_model()
# # create a plain load pattern
# pattern("Plain", 1, 1)
for j in range(0, numFloor + 1):

    xLoc = 0.
    for i in range(0, numBay + 1):
        node(nodeTag, xLoc, yLoc)
        # if i == 1:
        # load(nodeTag, load2, load2, 0.0)
        # else 
        # load(nodeTag, loa1, load1, 0.0)
        xLoc += bayWidth
        nodeTag += 1

    # if j < numFloor:
    #     storyHeight = storyHeights[j]

    yLoc += 3
   
# for j in range(0, 2):

#     xLoc = 0.

#     for i in range(0, numBay + 1):
#         node(nodeTag, xLoc, yyLoc)
#         # load(nodeTag, load2, load2, 0.0)
#         xLoc += bayWidth
#         nodeTag += 1

    
# opsv.plot_model()
    # yyLoc += -1.2
# load(10, -100, 50, 0.0)

# opsv.plot_loads_2d()
E = 29500000.0
mass1 = 10
mass2 = 10
mass3 = 10
loadgg=-100
M = 0.
coordTransf = "Linear"  # Linear, PDelta, Corotational
massType = "-lMass"  # -lMass, -cMass

beams = ['W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1','W1', 'W1','W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1','W1', 'W1']
eColumn = ['W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1','W1', 'W1']
iColumn =['W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1','W1', 'W1']
columns = [eColumn, iColumn,iColumn,iColumn,iColumn, eColumn]

WSection = {
    'W1': [0.25, 5.2e-3],
    'W14X287': [84.4, 3910.],
    'W24X110': [32.5, 3330.],
    'W24X130': [38.3, 4020.],
    'W24X160': [47.1, 5120.]
}


timeSeries("Linear", 1)

# create a plain load pattern
pattern("Plain", 1, 1)
for j in range(7, 247):
    mass(j, mass2, mass2, 1.0e-10)
    load(j, 0, loadgg, 1.0e-10)
    # for i in range(0, numBay + 1):

# procedure to read
def ElasticBeamColumn(eleTag, iNode, jNode, sectType, E, transfTag, M, massType):
    found = 0

    prop = WSection[sectType]

    A = prop[0]
    I = prop[1]
    element('elasticBeamColumn', eleTag, iNode, jNode, A, E, I, transfTag, '-mass', M, massType)


# add the nodes
#  - floor at a time

# fix first floor
# fix(1, 1, 1, 1)
# fix(2, 1, 1, 1)
# fix(3, 1, 1, 1)

# rigid floor constraint & masses
# nodeTagR = 2
# nodeTag = 1
# for j in range(1, numFloor + 1):
#     for i in range(0, numBay + 1):

#         if i== 1:
#             mass(nodeTagR, mass2, mass2, 1.0e-10)
#         else:
#             mass(nodeTagR, mass1, mass1, 1.0e-10)

#         nodeTag += 1

#     nodeTagR += numBay + 1
nodeTag=7


        # if i== 1:
        #     mass(nodeTagR, mass2, mass2, 1.0e-10)
        # else:
    

        # nodeTag += 1

  
# add the columns
# add column element
geomTransf(coordTransf, 1)
eleTag = 1
for j in range(0, numBay + 1):

    end1 = j + 1
    end2 = end1 + numBay + 1
    thisColumn = columns[j]

    for i in range(0, numFloor):
        secType = thisColumn[0]
        ElasticBeamColumn(eleTag, end1, end2, secType, E, 1, M, massType)
        end1 = end2
        end2 += numBay + 1
        eleTag += 1

# add beam elements
for j in range(1, numFloor + 1):
    end1 = (numBay + 1) * j + 1
    end2 = end1 + 1
    secType = beams[0]
    for i in range(0, numBay):
        ElasticBeamColumn(eleTag, end1, end2, secType, E, 1, M, massType)
        end1 = end2
        end2 = end1 + 1
        eleTag += 1

# calculate eigenvalues & print results
# for i in range(1,245,6):
#     equalDOF(i  , i+numBay, 1, 2)
# opsv.plot_model(node_labels=0, element_labels=0)
# for i in range(6):
#     fix(i+1, 1, 1, 1)


model('Basic', '-ndm', 2, '-ndf', 2)
xxx=[-45,-40,-35,-30,-25,-22.5,-20,-17.5,-15,-12.5,-10,-7.5,-5,-2.5,0,1.5,3,4.5,6,7.5,9,10.5,12,13.5,15,16.5,18,19.5,21,22.5,24,25.5,27,28.5,30,32.5,35,37.5,40,42.5,45,47.5,50,52.5,55,60,65,70,75]
lx=len(xxx)
yyy=[0.5,1,1.5,2.5]
yy=[11,5,3,11]
y=[11,5,3,10]
nx=lx
ny=72
yloc=0
layer=4
nodenum=501
for i in range(1,layer+1):
    for k in range(yy[i-1]):
        for j in range(0,nx):
            # if j%2==0:
            xloc=xxx[(int(j))]
            # else:
                # xloc=(xxx[(int((j-1)/2))]+xxx[(int((j+1)/2))])/2
          
            node(nodenum, xloc, yloc) 
            nodenum=nodenum+1
        yloc=yloc-yyy[i-1]

grade = 0
slope = mm.atan(grade/100.0)
g     = -9.81

xwgt_var = g * (mm.sin(slope))
ywgt_var = g * (mm.cos(slope))
thick = [1.0,1.0,1.0]
xWgt  = [xwgt_var, xwgt_var, xwgt_var] 
yWgt  = [ywgt_var, ywgt_var, ywgt_var] 
uBulk = [6.88E6,  5.06E6, 5.0E-6]
hPerm = [1.0E-4, 1.0E-4, 1.0E-4]
vPerm = [1.0E-4, 1.0E-4, 1.0E-4]

equalDOF(1, 515, 1, 2)
equalDOF(2, 519, 1, 2)
equalDOF(3, 523, 1, 2)
equalDOF(4, 527, 1, 2)
equalDOF(5, 531, 1, 2)
equalDOF(6, 535, 1, 2)

for i in range(1922,1971):
    fix(i,1,1)
for i in range(30):
    equalDOF(501+49*i, 549+49*i, 1, 2)
# nDMaterial PressureDependMultiYield02
# nDMaterial('PressureDependMultiYield02', matTag, nd, rho, refShearModul, refBulkModul,\
#    frictionAng, peakShearStra, refPress, pressDependCoe, PTAng,\
#        contrac[0], contrac[2], dilat[0], dilat[2], noYieldSurf=20.0,\
#            *yieldSurf=[], contrac[1]=5.0, dilat[1]=3.0, *liquefac=[1.0,0.0],e=0.6, \
#                *params=[0.9, 0.02, 0.7, 101.0], c=0.1)

nDMaterial('PressureDependMultiYield02',11, 2, 1.8, 9.0e4, 2.2e5, 32, 0.1, \
                                      101.0, 0.5, 26, 0.067, 0.23, 0.06, \
                                      0.27, 20, 5.0, 3.0, 1.0, \
                                      0.0, 0.77, 0.9, 0.02, 0.7, 101.0)

nDMaterial('PressureDependMultiYield02', 12, 2, 2.24, 9.0e4, 2.2e5, 32, 0.1, \
                                      101.0, 0.5, 26, 0.067, 0.23, 0.06, \
                                      0.27, 20, 5.0, 3.0, 1.0, \
                                      0.0, 0.77, 0.9, 0.02, 0.7, 101.0)
    
nDMaterial('PressureDependMultiYield02',13, 2, 2.45, 1.3e5, 2.6e5, 39, 0.1, \
                                      101.0, 0.5, 26, 0.010, 0.0, 0.35, \
                                      0.0, 20, 5.0, 3.0, 1.0, \
                                      0.0, 0.47, 0.9, 0.02, 0.7, 101.0) 
nDMaterial('ElasticIsotropic', 10, 3.1e7, 0.25)
# nDMaterial('ElasticIsotropic', 12, 3e6, 0.25)
# nDMaterial('ElasticIsotropic', 13, 3e6, 0.25)
elen=1001
# for i in range(1,layer+1):
for k in range(29):
    nI = 49*k+550
    nJ = 49*k+551
    nK = 49*k+502
    nL = 49*k+501
    
    for j in range(lx-1):
        if k <=2:
            if j> 13 and j <34:
                element('quad', elen, nI, nJ, nK, nL, thick[1], 'PlaneStrain', 10,0,2.5)
            else:
                element('quad', elen, nI, nJ, nK, nL, thick[1], 'PlaneStrain', 11)
        elif k>2 and k<=10:  
            element('quad', elen, nI, nJ, nK, nL, thick[1], 'PlaneStrain', 11)
        elif k>10 and k<=15:
            element('quad', elen, nI, nJ, nK, nL, thick[1],'PlaneStrain',  12)
        else:
            element('quad', elen, nI, nJ, nK, nL,   thick[1],'PlaneStrain', 13)
        nI=nI+1
        nJ=nJ+1
        nK=nK+1
        nL=nL+1
        elen=elen+1
        
dashF =10001
dashS =  10002

node(dashF,  -45, -40.0)
node(dashS,  -45, -40.0)

# define fixities for dashpot nodes
fix(dashF, 1, 1)
fix(dashS, 0, 1)

# define equal DOF for dashpot and base soil node
equalDOF(1922, dashS,  1)


# define dashpot material
colArea      = 2 * thick[0]
rockVS       = 700.0
rockDen      = 2.5
dashpotCoeff = rockVS * rockDen

#uniaxialMaterial('Viscous', matTag, C, alpha)
uniaxialMaterial('Viscous', 21, dashpotCoeff * colArea, 1)

# define dashpot element
element('zeroLength', 5001, dashF, dashS, '-mat', 21, '-dir', 1)

#---RAYLEIGH DAMPING PARAMETERS
# damping ratio
damp = 0.02
# lower frequency
omega1 = 2 * np.pi * 0.2
# upper frequency
omega2 = 2 * np.pi * 20
# damping coefficients
a0 = 2*damp*omega1*omega2/(omega1 + omega2)
a1 = 2*damp/(omega1 + omega2)



ModelData = opst.GetFEMdata(results_dir="opstool_output")
ModelData.get_model_data(save_file="ModelData.hdf5")
opsvis = opst.OpsVisPlotly(point_size=2, line_width=3, colors_dict=None, theme="plotly",
                            color_map="jet", on_notebook=True, results_dir="opstool_output")
# opsvis = opst.OpsVisPyvista(point_size=2, line_width=3,
#                             colors_dict=None, theme="paraview",
#                             color_map="coolwarm", on_notebook=False,
#                             results_dir="opstool_output")
opsvis.model_vis(input_file="ModelData.hdf5",
                  show_node_label=False,
                  show_ele_label=False,
                  show_local_crd=True,
                  show_fix_node=True,
                  show_constrain_dof=True,
                  label_size=8,
                  show_outline=True,
                  opacity=1.0,
                  save_html='modd2')

# Lambda = eigen('-fullGenLapack', 9)
# opsv.plot_model(node_labels=0, element_labels=0)
numEigen = 7
eigenValues = eigen(numEigen)
# PI = 2 * asin(1.0)

Nsteps = 10
wipeAnalysis()
system('BandGeneral')
constraints('Transformation')
numberer('RCM')
test('NormDispIncr', 1.0e-12, 10, 3)
algorithm('Newton')
integrator('LoadControl', 1 / Nsteps)
analysis('Static')
for i in range(Nsteps):
    ok = analyze(1)
    
loadConst('-time', 0.0)
timeSeries('Path', 2, '-dt', 0.01, '-filePath', 'BM68elc.acc', '-factor', 50.0)
pattern('UniformExcitation', 2, 1, '-accel', 2) #how to give accelseriesTag?

# eigen = eigen('-fullGenLapack', 9)
import math
power = math.pow(eigenValues[0], 0.5)
betaKcomm = 2 * (0.02/power)

# rayleigh(a0, 0.0, 0.0, betaKcomm)

wipeAnalysis()
constraints('Penalty', 1.0E16, 1.0E16)
numberer('RCM')
system('ProfileSPD')
rayleigh(a0, a1, 0.0, betaKcomm)
test('NormDispIncr', 1e-8, 100)
algorithm('Newton')
integrator('Newmark', 0.5, 0.25)
analysis('Transient')
for i in range(1,1001):
    if i%20==1:
        ok = analyze(1,0.01)
        ModelData.get_resp_step()
    else:
        ok = analyze(1,0.01)
    
# save all responses data after loop
ModelData.save_resp_all(save_file="RespStepData-1.hdf5")
opsvis.deform_vis(input_file="RespStepData-1.hdf5",
                  slider=True,
                  response="disp", alpha=None,
                  show_outline=False, show_origin=True,
                  show_face_line=False, opacity=1,
                  save_html='ff',
                  model_update=False)