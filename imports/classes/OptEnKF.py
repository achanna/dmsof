import sys
sys.path.append('../misc')
from header import *

class OptEnKF(Optimization):
  __mapper_args__ = {'polymorphic_identity':'EnKF'}
  def presample(self,args=None): return []
  def generate_sample(self,misc,args=None,runLocal=False):
    sample = Sample(optimization=self)
    self.setup_simulations(sample)
    for parameter in self.get_parameters():
      value    = parameter.get_pxd().priorModel.draw()
      estimate = Estimate(sample=sample,parameter=parameter,value=value)
      parameter.estimates.append(estimate)
    return sample
