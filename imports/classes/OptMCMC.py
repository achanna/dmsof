import sys
sys.path.append('../misc')
from header import *

class OptMCMC(Optimization):

  __mapper_args__ = {'polymorphic_identity':'MCMC'}

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
      acc_subj += [relate.sample_subj]
      acc_obj  += [relate.sample_obj]
    pro_subj=[]
    for relate in session.query(Relate).filter_by(relation='proposed'):
      pro_subj.append(relate.sample_subj)
    #print acc_obj
    #print acc_subj
    #print pro_subj
    output = list( set(acc_obj)-set(acc_subj)-set(pro_subj) )
    #print output
    return output

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
      if newLik<oldLik: A=1
      else: A = (newLik-oldLik)/oldLik
      u = np.random.random()
      if u<=A: relate.relation='accepted'
      else:    relate.relation='rejected'
      #if oldLik>newLik: print oldLik, newLik, A, relate.relation
      print oldLik, newLik, A, relate.relation

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
