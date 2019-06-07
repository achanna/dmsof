import sys
sys.path.append('../misc')
from header import *

class OptSpecified_pilot2(Optimization):

  __mapper_args__ = {'polymorphic_identity':'Specified_pilot2'}

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
    sample.misc=ests['ids']
    sample.push(runLocal)
    return []
