import sys
sys.path.append('../misc')
from header import *

class OptMC(Optimization):

  __mapper_args__ = {'polymorphic_identity':'MC'}

  def presample(self,args=None): return []

  def generate_sample(self,misc,args=None,runLocal=False):
    sample = Sample(optimization=self)
    self.setup_simulations(sample)
    constraints = self.get_constraints()
    if self.parameters==[]:
      pass
    for parameter in self.get_parameters():
      value    = parameter.get_pxd().priorModel.draw()
      estimate = Estimate(sample=sample,parameter=parameter,value=value)
      parameter.estimates.append(estimate)
    while True:
      for estimate in sample.estimates:
        estimate.value = estimate.parameter.get_pxd().priorModel.draw()
      if np.all([constraint.fn(sample) for constraint in constraints]): break
    sample.push(runLocal)
    return []
