import sys
sys.path.append('../misc')
from header import *

class OptSA(Optimization):

  __mapper_args__ = {'polymorphic_identity':'SA'}

  def presample(self,args=None): return []

  def generate_sample(self,misc,args=None,runLocal=False):
    parameters=self.parameters
    x0 = args['x0']
    for i in range(len(parameters)):
      min = parameters[i].get_pxd().priorModel.min
      max = parameters[i].get_pxd().priorModel.max
      values = np.linspace(min,max,100)
      for j in range(100):
        print i,j
        sample = Sample(optimization=self)
        self.setup_simulations(sample)
        for k in range(len(parameters)):
          if i==k: value = values[j]
          else:    value = x0[k]
          print parameters[k].get_pxd().domain.title, parameters[k].get_pxd().property.title, value
          estimate = Estimate(sample=sample,parameter=parameters[k],value=value)
          parameters[k].estimates.append(estimate)
        sample.push(runLocal)
    return []
