import sys
sys.path.append('../misc')
from header import *

class OptPareto(Optimization):

  __mapper_args__ = {'polymorphic_identity':'Pareto'}

  def startup(self): self.misc = {'dead_ids':[]}

  def presample(self,args=None):

    if 'objs' in args: objs = args['objs']
    else: objs = self.objectives

    samplesComplete = self.get_complete_samples()

    print 'total complete samples', len(samplesComplete)

    samples =[]
    for sample in samplesComplete:
      if not sample.id in self.misc['dead_ids']:
        samples += [sample]

    print 'total live samples', len(samples)

    dpar=self.crowding_distances_par(samples)
    dobj=self.crowding_distances_obj(samples,objs=objs,logErr=True)

    candidates = samples[:]
    fitness={}

    pop=[]
    for isample in candidates:
      isPareto = True
      for jsample in candidates:
        if isample==jsample: continue
        ierrs = isample.get_errors(objs)
        jerrs = jsample.get_errors(objs)
        le = np.less_equal(jerrs,ierrs)
        lt = np.less(jerrs,ierrs)
        if np.all(le) and np.any(lt):
          isPareto = False
          break
      if isPareto:
        fitness[isample.id]=0.5*(1-dpar[isample.id])+0.5*(1-dobj[isample.id])
        pop += [isample]

    return {'pop':pop,'fitness':fitness}

  def crowding_distances_obj(self,samples,objs=None,logErr=False):

    if type(objs)==type(None): objs = self.objectives

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

    pop     = misc['pop']
    fitness = misc['fitness']

    print self.id
    print [obj.id for obj in args['objs']]

    p=[]
    for sample in pop:
      p+=[1+fitness[sample.id]]

    sample = Sample(optimization=self)
    self.setup_simulations(sample)
    constraints = self.get_constraints()

    for parameter in self.get_parameters():
      estimate = Estimate(sample=sample,parameter=parameter,value=0)
      parameter.estimates.append(estimate)

    while True:
      p = p / np.sum(p)
      select = np.random.choice(pop,p=p)

      for estimate in sample.estimates:
        parentVal = select.get_estimates(estimate.parameter)[0].value
        var = estimate.parameter.get_pxd().priorModel.step
        estimate.value = np.random.normal(parentVal,var)

      if sample.is_within_bounds():
        if len(constraints)==0: break
        if np.all([constraint.fn(sample) for constraint in constraints]): break
    sample.push(runLocal)
    return [sample]
