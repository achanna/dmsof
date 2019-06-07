import sys
sys.path.append('../misc')
from header import *

class OptPareto(Optimization):

  __mapper_args__ = {'polymorphic_identity':'Pareto'}

  def presample(self,args=None):

    samples = self.get_complete_samples()

    dpar=self.crowding_distances_par(samples)
    dobj=self.crowding_distances_obj(samples,logErr=True)

    candidates = samples[:]
    pop=[]
    fitness={}
    ranks=[]
    rank=1
    while len(pop)<args['N']:

      front=[]
      for isample in candidates:
        isPareto = True
        for jsample in candidates:
          if isample==jsample: continue
          ierrs = isample.get_errors(self.objectives)
          jerrs = jsample.get_errors(self.objectives)
          le = np.less_equal(jerrs,ierrs)
          lt = np.less(jerrs,ierrs)
          if np.all(le) and np.any(lt):
            isPareto = False
            break
        if isPareto:
          front += [isample]
          candidates.remove(isample)
      if len(front)==0: break

      if (len(front)+len(pop))<=args['N']:
        pop   += front
        ranks += len(front)*[rank]
      else:
        dobjs = []
        for sample in front: dobjs += [dobj[sample.id]]
        ii = np.argsort(dobjs)
        for sample in np.array(front)[ii]: pop += [sample]
        ranks += ii*[rank]

      rank+=1
    pop   = pop[0:args['N']]
    ranks = ranks[0:args['N']]

    session = sqlalchemy.inspect(self).session
    session.commit()
    return {'pop':pop,'ranks':ranks,'dpar':dpar,'dobj':dobj}

  def crowding_distances_obj(self,samples,logErr=False):

    errors = []
    for sample in samples:
      errors += [sample.get_errors()]
    errors = np.array(errors)
    if logErr: errors = np.log10(errors)

    dists = np.zeros(errors.shape[0],dtype='float')
    for iObj in range(errors.shape[1]):
      for iSamp in range(errors.shape[0]):
        tErr = errors[iSamp,iObj]
        ilt  = np.where( errors[:,iObj]<errors[iSamp,iObj] )[0]
        igt  = np.where( errors[:,iObj]>errors[iSamp,iObj] )[0]
        if   len(ilt)>0 and len(igt)==0:
          lErr = np.max(errors[ilt,iObj])
          dists[iSamp] += 2*np.abs(lErr-tErr) / np.abs( np.max(errors[:,iObj])-np.min(errors[:,iObj]) )
        elif len(igt)>0 and len(ilt)==0:
          rErr = np.min(errors[igt,iObj])
          dists[iSamp] += 2*np.abs(rErr-tErr) / np.abs( np.max(errors[:,iObj])-np.min(errors[:,iObj]) )
        else:
          lErr = np.max(errors[ilt,iObj])
          rErr = np.min(errors[igt,iObj])
          dists[iSamp] += np.abs(rErr-lErr) / np.abs( np.max(errors[:,iObj])-np.min(errors[:,iObj]) )

    dists = dists / np.max(dists)
    output={}
    for i in range(len(samples)):
      output[samples[i].id] = dists[i]
    return output

  def crowding_distances_par(self,samples):

    values = []
    for sample in samples:
      values += [[]]
      for parameter in self.parameters:
        values[-1] += [sample.get_estimates(parameter)[0].value]
    values = np.array(values)

    dists = np.zeros(values.shape[0],dtype='float')
    for iObj in range(values.shape[1]):
      for iSamp in range(values.shape[0]):
        tErr = values[iSamp,iObj]
        ilt  = np.where( values[:,iObj]<values[iSamp,iObj] )[0]
        igt  = np.where( values[:,iObj]>values[iSamp,iObj] )[0]
        if   len(ilt)>0 and len(igt)==0:
          lErr = np.max(values[ilt,iObj])
          dists[iSamp] += 2*np.abs(lErr-tErr) / np.abs( np.max(values[:,iObj])-np.min(values[:,iObj]) )
        elif len(igt)>0 and len(ilt)==0:
          rErr = np.min(values[igt,iObj])
          dists[iSamp] += 2*np.abs(rErr-tErr) / np.abs( np.max(values[:,iObj])-np.min(values[:,iObj]) )
        else:
          lErr = np.max(values[ilt,iObj])
          rErr = np.min(values[igt,iObj])
          dists[iSamp] += np.abs(rErr-lErr) / np.abs( np.max(values[:,iObj])-np.min(values[:,iObj]) )

    dists = dists / np.max(dists)
    output={}
    for i in range(len(samples)):
      output[samples[i].id] = dists[i]
    return output

  def generate_sample(self,misc,args=None,runLocal=False):

    pop   = misc['pop']
    ranks = misc['ranks']
    dpar  = misc['dpar']
    dobj  = misc['dobj']

    print pop
    print ranks
    print len(pop)
    print len(ranks)
    exit()

    prob = []
    for sample in pop:
      prob += []

    oldSample = np.random.choice(pop,p=prob)

    sample = Sample(optimization=self)
    self.setup_simulations(sample)
    constraints = self.get_constraints()

    for parameter in self.get_parameters():
      estimate = Estimate(sample=sample,parameter=parameter,value=0)
      parameter.estimates.append(estimate)

    while True:
      for estimate in sample.estimates:
        parentVal = oldSample.get_estimates(estimate.parameter)[0].value
        var = estimate.parameter.get_pxd().priorModel.step*0.05
        estimate.value = np.random.normal(parentVal,var)

      if len(constraints)==0: break
      if np.all([constraint.fn(sample) for constraint in constraints]): break
    sample.push(runLocal)
    return [sample]
