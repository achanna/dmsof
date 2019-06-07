import sys
sys.path.append('../misc')
from header import *

class OptNSGAII(Optimization):

  __mapper_args__ = {'polymorphic_identity':'NSGAII'}

  def startup(self): self.misc = {'dead_ids':[]}

  def presample(self,args=None):

    samplesComplete = self.get_complete_samples()

    print 'total complete samples', len(samplesComplete)

    print len(self.misc['dead_ids']), len(np.unique(self.misc['dead_ids'])), min(self.misc['dead_ids']), max(self.misc['dead_ids'])

    samples=[]
    for sample in samplesComplete:
      if not sample.id in self.misc['dead_ids']:
        samples += [sample]

    print 'total live samples', len(samples)

    dpar=self.crowding_distances_par(samples)
    dobj=self.crowding_distances_obj(samples,args['objs'],logErr=True)

    candidates = samples[:]
    pop=[]
    fitness={}
    rank=1
    while len(pop)<args['N']:

      front=[]
      for isample in candidates:
        isPareto = True
        for jsample in candidates:
          if isample==jsample: continue
          ierrs = isample.get_errors(args['objs'])
          jerrs = jsample.get_errors(args['objs'])
          le = np.less_equal(jerrs,ierrs)
          lt = np.less(jerrs,ierrs)
          if np.all(le) and np.any(lt):
            isPareto = False
            break
        if isPareto:
          fitness[isample.id]=rank+0.5*(1-dpar[isample.id])+0.5*(1-dobj[isample.id])
          front += [isample]
          candidates.remove(isample)
      if len(front)==0: break

      if (len(front)+len(pop))<=args['N']: pop += front
      else:
        dobjs = []
        for sample in front: dobjs += [dobj[sample.id]]
        ii = np.argsort(dobjs)

        for sample in np.array(front)[ii]: pop += [sample]
      rank+=1
    pop = pop[0:args['N']]

    #for sample in samples:
    #  if sample not in pop:
    #    print 'ding dong sample %i is ded' % sample.id
    #    self.misc['dead_ids'] += [sample.id]

    session = sqlalchemy.inspect(self).session
    session.commit()
    return {'pop':pop,'fitness':fitness}

  def crowding_distances_obj(self,samples,objs,logErr=False):

    errors = []
    for sample in samples:
      errors += [sample.get_errors(objs)]
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
        elif len(igt)==0 and len(ilt)==0:
          dists[iSamp]=0
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
    values = np.reshape(np.array(values),[len(samples),len(self.parameters)])

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

    pop     = misc['pop']
    fitness = misc['fitness']
    k       = args['tournament_size']
    print self.id
    print [obj.id for obj in args['objs']]

    sample = Sample(optimization=self)
    self.setup_simulations(sample)
    constraints = self.get_constraints()

    for parameter in self.get_parameters():
      estimate = Estimate(sample=sample,parameter=parameter,value=0)
      parameter.estimates.append(estimate)

    while True:

      tournament = np.random.choice(pop,k)
      fits = []
      bestFitness = 1e99
      for candidate in tournament:
        if fitness[candidate.id]<bestFitness:
          p1 = candidate
          bestFitness = fitness[candidate.id]

      tournament = np.random.choice(pop,k)
      fits = []
      bestFitness = 1e99
      for candidate in tournament:
        if fitness[candidate.id]<bestFitness:
          p2 = candidate
          bestFitness = fitness[candidate.id]

      for estimate in sample.estimates:
        p = np.random.choice([p1,p2])
        parentVal = p.get_estimates(estimate.parameter)[0].value
        var = estimate.parameter.get_pxd().priorModel.step
        estimate.value = np.random.normal(parentVal,var)

      if sample.is_within_bounds():
        if len(constraints)==0: break
        if np.all([constraint.fn(sample) for constraint in constraints]): break
      else:
        print 'sample out of bounds'

    sample.push(runLocal)
    return [sample]
