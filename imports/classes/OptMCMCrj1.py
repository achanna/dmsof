import sys
sys.path.append('../misc')
from header import *

class OptMCMCrj1(Optimization):

  __mapper_args__ = {'polymorphic_identity':'MCMCrj1'}

  def create_chains(self,nn,map,runLocal=False):
    for i in range(map.shape[0]):
      sample = Sample(optimization=self)
      self.setup_simulations(sample)
      for parameter in self.MCMCrj_parameterization(map[i,:]):
        value    = parameter.get_pxd().priorModel.draw()
        estimate = Estimate(sample=sample,parameter=parameter,value=value)
        parameter.estimates.append(estimate)
      sample.misc = {'stepMod':1.0}
      sample.push(runLocal)
      relate = Relate( relation='accepted', optimization=self, sample_obj=sample )

  def MCMCrj_parameterization(self,lens):
    params=[]
    for domain in self.get_domains():
      if domain.title=='Lens':
        pp = np.random.uniform(0,2000,size=[50,2])
        ii = np.where(((pp[:,0]-lens[0])**2+(pp[:,1]-lens[1])**2)**0.5<lens[2])[0]
        cc  = np.zeros([pp.shape[0],1])
        cc[ii] += 1
        geom = np.concatenate([pp,cc],axis=1)
      else:
        geom  = domain.generate_geometry()
      struc = Structure( domain=domain, geom=geom )
      for pxd in domain.pxds:
        params.append( Parameter(structure=struc,property=pxd.property) )
    return params

  def presample(self,args=None):
    return self.fetch_terminal_samples()

  def generate_sample(self,terminal_samples,args=None,runLocal=False):
    # attempts to locate an MCMC chain ready for another iteration
    # if none exists, simply end function and move on
    if len(terminal_samples)==0: return []
    oldSample = np.random.choice(terminal_samples,1)[0]
    terminal_samples.remove(oldSample)
    newSample = oldSample.copy()
    estimate = np.random.choice(newSample.estimates)
    estimate.value = estimate.parameter.get_pxd().priorModel.perturb(estimate.value,oldSample.misc['stepMod'])
    newSample.push(runLocal)
    relate = Relate( relation='proposed', optimization=self, sample_subj=oldSample, sample_obj=newSample )
    return []

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
      else: A = 1+50*(newLik-oldLik)/oldLik
      u = np.random.random()
      if u<=A: relate.relation='accepted'
      else:    relate.relation='rejected'

      if oldLik>newLik: print oldLik, newLik, A, relate.relation

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
