import sys
sys.path.append('../misc')
from header import *

class OptSimAnn(Optimization):

  __mapper_args__ = {'polymorphic_identity':'SimAnn'}

  def presample(self,args=None):

    if 'objs' in args: objs = args['objs']
    else: objs=None
    complete = self.get_complete_samples()
    if len(complete)>args['mSamples']: complete = np.random.choice(complete,args['mSamples'])
    else: args['mSamples']=len(complete)
    paretoRanks = start_pareto_rank_structure(complete,objs)
    rankFitness = []
    for sample in complete: rankFitness += [1.0 / float(paretoRanks[sample.id])]
    return {'complete':complete,'rankFitness':rankFitness}

  def generate_sample(self,misc,args=None,runLocal=False):

    complete    = misc['complete']
    rankFitness = misc['rankFitness']

    newSample = Sample(optimization=self)
    self.setup_simulations(newSample)
    for parameter in self.get_parameters():
      value = parameter.get_pxd().priorModel.draw()
      estimate = Estimate(sample=newSample,parameter=parameter,value=value)
      parameter.estimates.append(estimate)

    if len(complete)>0:
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
        for sample in complete:
          values = np.vstack([ values, np.array([estimate.value for estimate in sample.estimates]).reshape(1,len(self.get_parameters())) ])
        proposed=self.normalizeEstimates(self.parameters,proposed)
        values=self.normalizeEstimates(self.parameters,values)

        f  = scipy.interpolate.NearestNDInterpolator( values, rankFitness )
        ri = np.zeros(len(proposed),dtype='float')
        for i in range(len(proposed)):
          ri[i] = f(proposed[i])

        di = np.zeros(len(proposed))
        for i in range(proposed.shape[0]):
          di[i] = 1e99
          minDist=np.inf
          for j in range(values.shape[0]):
            thisDist = np.sum((proposed[i,:]-values[j,:])**2)**0.5
            if thisDist<di[i]: di[i]=thisDist

        pi  = 0.9*ri/np.sum(ri) + 0.1*di/np.sum(di)
        pi  = np.multiply( ri/np.sum(ri), di/np.sum(di) )
        pi /= np.sum(pi)

        best = np.random.choice(len(proposed),1,p=pi)[0]

      for i in range(len(newSample.estimates)):
        prior = newSample.estimates[i].parameter.get_pxd().priorModel
        newSample.estimates[i].value = proposed[best,i] * (prior.max-prior.min) + prior.min
    newSample.push(runLocal)
    return [newSample]
