import sys
sys.path.append('../misc')
from header import *

class OptSpecified_pilot(Optimization):

  __mapper_args__ = {'polymorphic_identity':'Specified_pilot'}

  def presample(self,args=None): return []

  def generate_sample(self,misc,args=None,runLocal=False):
    ests = args['ests']
    sample = Sample(optimization=self)
    self.setup_simulations(sample)
    constraints = self.get_constraints()
    parameters = self.get_parameters()
    for param in parameters:
      value = ests[param.structure.domain.id][param.property.id]
      estimate = Estimate(sample=sample,parameter=param,value=value)
      param.estimates.append(estimate)
    lensElements=[]
    xyz  = pickle.load( open('mesh.pkl','rb') )['hex_xyzs']
    ii = np.where(np.multiply(xyz[:,2]>-5,xyz[:,2]<0))[0]
    xy = xyz[ii,0:2]

    cx=ests[2][5]
    cy=ests[2][6]
    el=ests[2][7]
    ew=ests[2][8]
    ea=ests[2][9]

    z=[]
    for i in range(xy.shape[0]):
      wx = xy[i,0]
      wy = xy[i,1]
      cos_angle = np.cos(np.radians(180.-ea))
      sin_angle = np.sin(np.radians(180.-ea))
      xc0 = wx - cx
      yc0 = wy - cy
      xct = xc0 * cos_angle - yc0 * sin_angle
      yct = xc0 * sin_angle + yc0 * cos_angle
      rad_cc = (xct**2/(el/2.)**2) + (yct**2/(ew/2.)**2)
      if rad_cc<1: z+=[1]
      else:        z+=[0]
    z  = np.array(z)
    sample.misc=np.where(z==1)[0]
    sample.push(runLocal)
    return []
