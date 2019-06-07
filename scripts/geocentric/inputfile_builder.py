import pickle
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import scipy
import scipy.interpolate
import sys

def polynomial_to_string(t,d):
  string=''
  string += '(t<%f)*(%e)+' % (t[0]*86400,d[0])
  for i in range(len(t)-1):
    string += '(%f<=t)*(t<%f)*(%e)+' % (t[i]*86400,t[i+1]*86400,d[i])
  string += '(t>=%f)*(%e)\n' % (t[-1]*86400,d[-1])
  return string[:-1]

data     = np.loadtxt('2017284-2017290_9a_injection.txt',delimiter=',')
t        = (data[:,0]-data[0,0])/3600.0/24.0
t        = (data[:,0]-data[0,0])
inj_rate = data[:,10] / (np.pi*1.8**2)

t  -= 5*86400.0

mu  = 2
vr  = 0.25
mag = 12e-5
lam = 2.5

t2 = np.linspace(0,17*86400.0,1000)
t0 = 2
t1 = 8
k1 = 6
k2 = 6
f2 = 6e-5* 1/(1+np.exp(-k1*((t2/86400.0-t0))))*(1- 1/(1+np.exp(-k2*((t2/86400.0-t1))))) + mag * np.exp( - ((t2/86400.0-mu))**2 / (2*vr**2) )
f2 = 6e-5* 1/(1+np.exp(-k1*((t2/86400.0-t0))))*(1- 1/(1+np.exp(-k2*((t2/86400.0-t1)))))

#inj_string = '6e-5*1/(1+exp(-6.0*((t/86400.0-2.0))))*(1-1/(1+exp(-3.0*((t/86400.0-8.0))))) + 12e-5 * exp( -1* ((t/86400.0-2.0))^2 / (2*0.25^2) )'
inj_string = '6e-5* 1/(1+exp(-3.0*((t/86400.0-2.0))))*(1-1/(1+exp(-3.0*((t/86400.0-8.0)))))'
#inj_string = '(t<(1*86400))*6e-5*t/(1.0*86400.0)+(t>(1*86400))*(t<=(7*86400))*(6e-5)'

plt.figure()
plt.plot(t,inj_rate)
plt.plot(t2,f2)
#plt.xlim([1,16])
plt.xlabel('Time [days]',fontsize=18)
plt.ylabel('Injection Rate [m/s]',fontsize=18)
plt.savefig('injection_rate.eps',format='eps',bbox_inches='tight')
plt.close()

k1 = -12.307
k2 = -14.307
k3 = -17.006
K1 = 2.0
K2 = 8.0
K3 = 2.9
cx = 0
cy = 0
lr = 200

hex_ids   = pickle.load( open('mesh.pkl','rb') )['hex_ids']
hex_xyzs  = pickle.load( open('mesh.pkl','rb') )['hex_xyzs']
hex_types = pickle.load( open('mesh.pkl','rb') )['hex_types']

file = open('input.geo','w')
file.write('SOLVER\n')
file.write('{\n')
file.write('  TYPE poromechanics\n')
file.write('  DISCRETIZATION cg\n')
file.write('  DIMENSION 3\n')
file.write('}\n')
file.write('MESH\n')
file.write('{\n')
file.write('  TYPE external_file\n')
file.write('  FILE_NAME mesh.inp\n')
file.write('  FILE_FORMAT inp\n')
file.write('  REFINEMENT 0\n')
file.write('}\n')
file.write('WATCH\n')
file.write('{\n')
file.write('  START_TIME 0\n')
file.write('  END_TIME 604800\n')
file.write('  TIMESTEPS 40\n')
file.write('  TIMESTEP_GROWTH_FACTOR 1.05\n')
file.write('  START_TIME2 604800\n')
file.write('  END_TIME2 1209600\n')
file.write('  TIMESTEPS2 40\n')
file.write('  TIMESTEP_GROWTH_FACTOR2 1.05\n')
file.write('}\n')
file.write('MATERIALS\n')
file.write('{\n')
for i in range(hex_ids.shape[0]):
  ivol  = hex_ids[i,0]
  iblk  = hex_ids[i,1]
  ihex  = hex_ids[i,2]
  x,y,z = hex_xyzs[i]
  type  = hex_types[i]

  nu    = 0.25
  phi   = 0.20
  Ks    = 42.9e9
  Kf    = 2.5e9

  if type==0 and z>=-5:
    kappa = 10**-11
    K     = 3e9
  elif type==1 and z>=0:
    kappa = 10**-99
    K     = 200e9
  elif type==1 and z>=-5:
    kappa = 10**-11
    K     = 200e9
  elif (type==2 and ((x-cx)**2+(y-cy)**2)**0.5<=lr):
#  elif (type==2 and (-500<x<80 and -150<y<150)):
    kappa = 10**k1
    K     = K1*1e9
  elif type==3:
    kappa = 10**k2
    K     = K2*1e9
  else:
    kappa = 10**k3
    K     = K3*1e9

  aB    = 1 - K / Ks
  M     = 1 / ( (aB-phi)/Ks + (phi/Kf) )

  file.write('  MATERIAL_%i\n' % iblk)
  file.write('  {\n')
  file.write('    SOLID_MODEL_TYPE linear_elastic\n')
  file.write('    BULK_MODULUS %e\n' % K)
  file.write('    POISSON_RATIO %f\n' % nu)
  file.write('    BIOT_COEFFICIENT %f\n' % aB)
  file.write('    BIOT_MODULUS %e\n' % M)
  file.write('    PERMEABILITY %e\n' % kappa)
  file.write('    VISCOSITY 8.900000e-04\n')
  file.write('    POROSITY %f\n' % phi)
  file.write('    SOLID_DENSITY 0.000000\n')
  file.write('    FLUID_DENSITY 0.000000\n')
  file.write('  }\n')

file.write('}\n')
file.write('BOUNDARY_CONDITIONS\n')
file.write('{\n')

file.write( '  BOUNDARY_1 { PRESSURE 0 }\n' )
file.write( '  BOUNDARY_2 { PRESSURE 0 }\n' )
file.write( '  BOUNDARY_3 { PRESSURE 0 }\n' )
file.write( '  BOUNDARY_4 { PRESSURE 0 }\n' )
file.write( '  BOUNDARY_5 { PRESSURE 0 }\n' )
#file.write( '  BOUNDARY_6 { PRESSURE 0 }\n' )
#file.write( '  BOUNDARY_6 { FLUX 0 }\n' )
#file.write( '  BOUNDARY_7 { PRESSURE 1e6 }\n' )
#file.write( '  BOUNDARY_7 { PRESSURE "%s" }\n' % p_string )
file.write( '  BOUNDARY_7 { FLUX "%s" }\n' % inj_string )

file.write( '  BOUNDARY_1  { NORMAL_DISPLACEMENT 0 }\n' )
file.write( '  BOUNDARY_2  { NORMAL_DISPLACEMENT 0 }\n' )
file.write( '  BOUNDARY_3  { NORMAL_DISPLACEMENT 0 }\n' )
file.write( '  BOUNDARY_4  { NORMAL_DISPLACEMENT 0 }\n' )
file.write( '  BOUNDARY_5  { NORMAL_DISPLACEMENT 0 }\n' )

file.write('}\n')
file.write('PARAMETERS\n')
file.write('{\n')
file.write('  CONVERGENCE\n')
file.write('  {\n')
file.write('    PROBLEM_IS_LINEAR true\n')
file.write('    KRYLOV_TOLERANCE 1e-4\n')
file.write('    MAX_KRYLOV_ITERATIONS 50000\n')
file.write('    NEWTON_TOLERANCE 1e-5\n')
file.write('    MAX_NEWTON_ITERATIONS 10\n')
file.write('  }\n')
file.write('  PRECONDITIONER\n')
file.write('  {\n')
file.write('    TYPE ilu\n')
file.write('    AMG\n')
file.write('    {\n')
file.write('      SMOOTHER_TYPE "ILU"\n')
file.write('      SMOOTHER_SWEEPS 1\n')
file.write('      COARSE_TYPE "Amesos-KLU"\n')
file.write('      USE_W_CYCLE true\n')
file.write('      AGGREGATION_THRESHOLD 1e-2\n')
file.write('    }\n')
file.write('    ILU\n')
file.write('    {\n')
file.write('      FILL 0\n')
file.write('    }\n')
file.write('  }\n')
file.write('  VISUALIZATION\n')
file.write('  {\n')
file.write('    WRITE_OUTPUT true\n')
file.write('    FILE_BASE_NAME "solution"\n')
file.write('    SAMPLE_POINTS\n')
file.write('    {\n')
file.write('      POINT_01 "%f %f %f"\n'  % (+239.8,  -75.3,  +495.0) )
file.write('      POINT_02 "%f %f %f"\n'  % (+374.6, -199.1,  +15.0) )
file.write('      POINT_03 "%f %f %f"\n'  % (-375.9,   -5.4,  +15.0) )
file.write('      POINT_04 "%f %f %f"\n'  % (-185.0,  +28.7,  +15.0) )
file.write('      POINT_05 "%f %f %f"\n'  % (-245.0, -111.7,  +15.0) )
file.write('      POINT_06 "%f %f %f"\n'  % (  +0.0,   -0.0,  +15.0) )
file.write('      POINT_07 "%f %f %f"\n'  % (+206.8,  -60.5,  +15.0) )
file.write('    }\n')
file.write('  }\n')
file.write('  BOUNDARY_PENALTY 1e10\n')
file.write('}\n')

file.close()

