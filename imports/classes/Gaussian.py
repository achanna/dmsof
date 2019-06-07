from StatModel import *
import numpy as np

class Gaussian(StatModel):

  def __init__(self,min,max,step,sig,mu):
    StatModel.__init__(self,min,max,step)
    self.sig = sig
    self.mu  = mu

  def draw(self):
    while True:
      draw = np.random.normal(self.sig,self.mu,1)[0]
      if draw>=self.min and draw<=self.max:
        return draw

  def perturb(self,value,stepMod=1.0):
    while True:
      perturbed = np.random.normal(value,self.step*stepMod)
      if perturbed>=self.min and perturbed<=self.max:
        return perturbed
