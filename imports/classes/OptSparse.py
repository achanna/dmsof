import sys
sys.path.append('../misc')
from header import *

class OptSparse(Optimization):

  __mapper_args__ = {'polymorphic_identity':'Sparse'}

  def presample(self,args=None): return []

  def generate_sample(self,misc,args=None,runLocal=False):
    newSample = Sample(optimization=self)
    self.setup_simulations(newSample)
    for parameter in self.get_parameters():
      value = parameter.get_pxd().priorModel.draw()
      estimate = Estimate(sample=newSample,parameter=parameter,value=value)
      parameter.estimates.append(estimate)
    pushed = self.get_pushed_samples()
    if len(pushed)>args['mSamples']: pushed = np.random.choice(pushed,args['mSamples'])
    else: args['mSamples']=len(pushed)
    if len(pushed)>0:
      proposed=[]
      for i in range(args['nSamples']):
        while True:
          for estimate in newSample.estimates:
            estimate.value = estimate.parameter.get_pxd().priorModel.draw()
          if np.all([constraint.fn(newSample) for constraint in self.get_constraints()]):
             this = [estimate.value for estimate in newSample.estimates]
             proposed.append(this)
             break
      proposed=np.array(proposed)
      if args['method']=='distance':
        values=np.zeros([0,len(self.get_parameters())],dtype='float')
        for sample in pushed:
          values = np.vstack([ values, np.array([estimate.value for estimate in sample.estimates]).reshape(1,len(self.get_parameters())) ])
        proposed=self.normalizeEstimates(self.parameters,proposed)
        values=self.normalizeEstimates(self.parameters,values)
        maxDist=0
        for i in range(proposed.shape[0]):
          minDist=np.inf
          for j in range(values.shape[0]):
            thisDist = np.sum((proposed[i,:]-values[j,:])**2)**0.5
            if thisDist<minDist: minDist=thisDist
          if minDist>maxDist:
            maxDist=minDist
            uniquestModel=proposed[i,:]
      for i in range(len(newSample.estimates)):
        prior = newSample.estimates[i].parameter.get_pxd().priorModel
        newSample.estimates[i].value = uniquestModel[i] * (prior.max-prior.min) + prior.min
    newSample.push(runLocal)
    return [newSample]
