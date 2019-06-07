import sys
sys.path.append('../misc')
from header import *

class OptSpecified(Optimization):

  __mapper_args__ = {'polymorphic_identity':'Specified'}

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
    sample.push(runLocal)
    return []
