import sys
sys.path.append('../misc')
from header import *

class OptMCMCrj(Optimization):

  __mapper_args__ = {'polymorphic_identity':'MCMCrj'}

  def create_chain(self,nn=1,runLocal=False):
    for i in range(nn):
      sample = Sample(optimization=self)
      self.setup_simulations(sample)
      for parameter in self.get_parameters():
        value    = parameter.get_pxd().priorModel.draw()
        estimate = Estimate(sample=sample,parameter=parameter,value=value)
        parameter.estimates.append(estimate)
      sample.misc = {'stepMod':1.0}
      sample.push(runLocal)
      relate = Relate( relation='accepted', optimization=self, sample_obj=sample )

  def presample(self,args=None):
    return self.fetch_terminal_samples()

  def generate_sample(self,terminal_samples,args=None,runLocal=False):
    # attempts to locate an MCMC chain ready for another iteration
    # if none exists, simply end function and move on
    t0=time.time()
    if len(terminal_samples)==0: return []
    oldSample = np.random.choice(terminal_samples,1)[0]
    terminal_samples.remove(oldSample)
    t1=time.time()
    newSample = oldSample.copy()
    t2=time.time()
    choice = np.random.random()
    t3=time.time()
    if 0 < choice and choice < 0.05:
      estimate = np.random.choice(newSample.estimates)
      for heterogeneity in estimate.parameter.structure.domain.heterogeneities:
        if heterogeneity.optimization==self: break
      if heterogeneity.spatial[0]<len(newSample.estimates) and len(newSample.estimates)<heterogeneity.spatial[1]:
        session = sqlalchemy.inspect(self).session
        session.delete(estimate)
    t4=time.time()
    if 0.05 < choice and choice < 0.10:
      oldEstimate  = np.random.choice(newSample.estimates)
      for heterogeneity in oldEstimate.parameter.structure.domain.heterogeneities:
        if heterogeneity.optimization==self: break
      if heterogeneity.spatial[0]<len(newSample.estimates) and len(newSample.estimates)<heterogeneity.spatial[1]:
        oldParameter = oldEstimate.parameter
        oldStructure = oldParameter.structure
        oldDomain    = oldStructure.domain
        oldGeom      = oldStructure.geom
        range        = oldDomain.geom[:,1]-oldDomain.geom[:,0]
        newGeom      = np.copy(oldGeom)+np.multiply( range, np.random.normal(0,0.01,oldGeom.shape) )
        newStructure = Structure( domain=oldDomain, geom=newGeom )
        newParameter = Parameter( structure=newStructure, property=oldParameter.property )
        newEstimate  = Estimate( sample=newSample, parameter=newParameter, value=oldEstimate.value )
    t5=time.time()
    if 0.10 < choice and choice < 0.55:
      estimate = np.random.choice(newSample.estimates)
      estimate.value = estimate.parameter.get_pxd().priorModel.perturb(estimate.value,oldSample.misc['stepMod'])
    t6=time.time()
    if 0.55 < choice and choice < 1.00:
      oldEstimate  = np.random.choice(newSample.estimates)
      oldParameter = oldEstimate.parameter
      oldStructure = oldParameter.structure
      oldDomain    = oldStructure.domain
      oldGeom      = oldStructure.geom
      range        = oldDomain.geom[:,1]-oldDomain.geom[:,0]
      while True:
        newGeom = np.copy(oldGeom)+np.multiply( range, newSample.misc['stepMod']*np.random.normal(0,0.05,oldGeom.shape) )
        if np.all(oldDomain.geom[:,0]<newGeom) and np.all(newGeom<oldDomain.geom[:,1]): break
      newStructure = Structure( domain=oldDomain, geom=newGeom )
      newParameter = Parameter( structure=newStructure, property=oldParameter.property )
      oldEstimate.parameter = newParameter
    t7=time.time()
    newSample.push(runLocal)
    t8=time.time()
    relate = Relate( relation='proposed', optimization=self, sample_subj=oldSample, sample_obj=newSample )
    t9=time.time()
    return [np.array([t0,t1,t2,t3,t4,t5,t6,t7,t8,t9])]

  def fetch_terminal_samples(self):
    # traverse samples in a random sequence (ie, iterate chains evenly over time)
    session = sqlalchemy.inspect(self).session
    acc_subj=[]
    acc_obj=[]
    for relate in session.query(Relate).filter_by(relation='accepted'):
      acc_subj.append(relate.sample_subj)
      acc_obj.append(relate.sample_obj)
    pro_subj=[]
    for relate in session.query(Relate).filter_by(relation='proposed'):
      pro_subj.append(relate.sample_subj)
    return list( set(acc_obj)-set(acc_subj)-set(pro_subj) )

  def metropolis_hastings(self):
    # find proposed samples, iterate
    session = sqlalchemy.inspect(self).session
    for relate in session.query(Relate).filter_by(relation='proposed').all():
      # find predecessors
      # find/compute likelihood of proposal and predecessor
      # accept or reject proposed sample

      oldSample = relate.sample_subj
      newSample = relate.sample_obj
      if oldSample.status()!=2 or newSample.status()!=2: continue

      oldLik = oldSample.likelihood_unnormalized()
      newLik = newSample.likelihood_unnormalized()
      if newLik>oldLik: A=1
      else: A = 1+700*(newLik-oldLik)/oldLik
      u = np.random.random()
#      print newSample.misc['stepMod']
      if u<=A:
        relate.relation='accepted'
#        if newSample.misc['stepMod']<10:
#          newSample.misc['stepMod'] *= 1.001
      else:
        relate.relation='rejected'
#        if newSample.misc['stepMod']>0.01:
#          newSample.misc['stepMod'] *= 0.999
#      print newSample.misc['stepMod']
      if oldLik>newLik: print oldLik, newLik, A, relate.relation

#      oldErr = oldSample.get_weighted_error()
#      newErr = newSample.get_weighted_error()
#      if newErr<oldErr:                               relate.relation='accepted'
#      elif np.random.random()<(newErr-oldErr)/oldErr: relate.relation='accepted'
#      else:                                           relate.relation='rejected'

  def get_chains(self):
    # find initial link of each chain
    chains=[]
    session = sqlalchemy.inspect(self).session
    for relate in session.query(Relate).filter_by(sample_subj=None).all():
      newChain = [relate.sample_obj]
      while True:
        next = session.query(Relate).filter_by(sample_subj=newChain[-1]).filter_by(relation='accepted').all()
        if len(next)==1:
          newChain.append( next[0].sample_obj )
        else: break
      chains.append(newChain)
    return chains
