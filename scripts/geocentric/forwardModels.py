import sys
sys.path.append('/home/achanna/Dropbox/poroelast7/imports/misc')
from header import *
from connect_info import *

def polynomial_to_string(t,d):
  string=''
  string += '(t<%f)*(%e)+' % (t[0],d[0])
  for i in range(len(t)-1):
    string += '(%f<=t)*(t<%f)*(%e)+' % (t[i],t[i+1],d[i])
  string += '(t>=%f)*(%e)\n' % (t[-1],d[-1])
  return string[:-1]

def assemble_model(simulation):
  model = []
  for estimate in simulation.sample.estimates: model.append(estimate.value)
  for prediction in simulation.predictions:
    model.append( prediction.id )
    for coord in prediction.objective.instrument.geom:
      model.append( coord )
    model.append( prediction.objective.instrument.instType.abv )
    model.append( 0 )
    model[-1] = prediction.objective.instrument.indVars
  return model

def plane(x, y, params):
  a = params[0]
  b = params[1]
  c = params[2]
  z = a*x + b*y + c
  return z

def error(params, points):
  result = 0
  for (x,y,z) in points:
    plane_z = plane(x, y, params)
    diff = abs(plane_z - z)
    result += diff**2
  return result

def cross(a, b):
  return [a[1]*b[2] - a[2]*b[1],
    a[2]*b[0] - a[0]*b[2],
    a[0]*b[1] - a[1]*b[0]]

def np2pwlinearstr(t,p):
  str=''
  str+= '(t<%f)*%f' % (t[0],p[0])
  for i in range(len(t)):
    str += '+(%f<t)*(t<%f)*(%f+(t-%f)*(%f-%f)/(%f-%f))' % (t[i-1],t[i],p[i-1],t[i-1],p[i],p[i-1],t[i],t[i-1])
  str += '+(%f<t)*%f' % (t[-1],p[-1])
  return str

def bdry_grad_3pt(points):
  fun = functools.partial(error, points=points)
  params0 = [0, 0, 0]
  res = scipy.optimize.minimize(fun, params0)
  point  = np.array([0.0, 0.0, res.x[2]])
  normal = np.array(cross([1,0,res.x[0]], [0,1,res.x[1]]))
  d = -point.dot(normal)
  str = '((%f*x)+(%f)*y+(%f))*(1/(%f))' % (-normal[0],-normal[1],-d,normal[2])
  return str

def buildInput(model):

  t0 = time.time()

  inj_string = '6.5e-5 * 1/(1+exp(-50*((t/86400.0-0.2))))*(1-1/(1+exp(-12*((t/86400.0-6.2))))) + 11e-5* exp( - ((t/86400.0-0.2))^2 / (2*0.05^2) ) + 0.35e-5 * exp( - ((t/86400.0-3.95))^2 / (2*0.9^2) )'

  for key, value in model['estimates'].iteritems():
    if value['domain']=='Lens':
      if value['abv']=='kappa': k1   = value['value']
      if value['abv']=='K':     K1   = value['value']
      if value['abv']=='phi':   phi1 = value['value']
      if value['abv']=='nu':    nu1  = value['value']
      if value['abv']=='cx':    cx   = value['value']
      if value['abv']=='cy':    cy   = value['value']
      if value['abv']=='lr':    lr   = value['value']
    if value['domain']=='Formation':
      if value['abv']=='kappa': k2   = value['value']
      if value['abv']=='K':     K2   = value['value']
      if value['abv']=='phi':   phi2 = value['value']
      if value['abv']=='nu':    nu2  = value['value']
    if value['domain']=='Confining':
      if value['abv']=='kappa': k3   = value['value']
      if value['abv']=='K':     K3   = value['value']
      if value['abv']=='phi':   phi3 = value['value']
      if value['abv']=='nu':    nu3  = value['value']

  print k1,k2,k3
  print K1,K2,K3
  print phi1,phi2,phi3
  print nu1,nu2,nu3
  print cx,cy,lr
  #exit()

  os.system('rm input-files.tgz input.geo')
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
  file.write('  END_TIME 518400\n')
  file.write('  TIMESTEPS 20\n')
  file.write('  TIMESTEP_GROWTH_FACTOR 1.13\n')
  file.write('  START_TIME2 518400\n')
  file.write('  END_TIME2 1468800\n')
  file.write('  TIMESTEPS2 15\n')
  file.write('  TIMESTEP_GROWTH_FACTOR2 1.11\n')
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
    Kf    = 2.15e9

    if type==0 and z>=-7:
      kappa = 10**-11
      K     = 3e9
      nu    = 0.30
      phi   = 0.8
    elif type==1 and z>=0:
      kappa = 10**-99
      K     = 200e9
      Ks    = 200e9
      nu    = 0.30
      phi   = 0.0001
    elif type==1 and z>=-7:
      kappa = 10**-11
      K     = 200e9
      Ks    = 200e9
      Kf    = 2.15e9
      nu    = 0.30
      phi   = 0.8
    elif (type==2 and ((x-cx)**2+(y-cy)**2)**0.5<=lr):
      kappa = 10**k1
      K     = K1*1e9
      phi   = phi1
      nu    = nu1
    elif type==3:
      kappa = 10**k2
      K     = K2*1e9
      phi   = phi2
      nu    = nu2
    else:
      kappa = 10**k3
      K     = K3*1e9
      phi   = phi3
      nu    = nu3

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
  points = [(+6000,-1000,0),
            (-2000,-1300,0),
            (+7000,+3000,0),
            (-1000,+4000,0),
            (-1700,+6000,0)]
  str1=bdry_grad_3pt(points)

  file.write( '  BOUNDARY_1  { PRESSURE 0 }\n' )
  file.write( '  BOUNDARY_2  { PRESSURE 0 }\n' )
  file.write( '  BOUNDARY_3  { PRESSURE 0 }\n' )
  file.write( '  BOUNDARY_4  { PRESSURE 0 }\n' )
  file.write( '  BOUNDARY_5  { FLUX 0 }\n' )
  file.write( '  BOUNDARY_7  { FLUX "%s" }\n' % inj_string )

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
  file.close()

  pickle.dump({'model':model},open('model.pkl','wb'))
  os.system('tar cvzf input-files.tgz input.geo model.pkl > /dev/null 2>&1')
  print 'forward model: ', time.time()-t0
