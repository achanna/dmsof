from StatModel import *
import numpy as np

class Uniform(StatModel):

  def __init__(self,min,max,step):
    StatModel.__init__(self,min,max,step)

  def draw(self):
    return np.random.uniform(self.min,self.max,1)[0]

  def perturb(self,value,stepMod=1.0):
    while True:
      perturbed = np.random.normal(value,self.step*stepMod)
      if perturbed>=self.min and perturbed<=self.max:
        return perturbed
