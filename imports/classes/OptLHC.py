import sys
sys.path.append('../misc')
from header import *

class OptLHC(Optimization):

  __mapper_args__ = {'polymorphic_identity':'LHC'}

  def startup(self,n):
    parameters = self.parameters
    ests = pyDOE.lhs( len(parameters), samples=n, criterion='corr' )
    sample = Sample(optimization=self)
    for param in parameters:
      estimate = Estimate(sample=sample,parameter=param,value=0)
      param.estimates.append(estimate)
    constraints = self.get_constraints()
#    parameters = self.get_parameters()
    if len(constraints)>0:
      good=[]
      for i in range(len(ests)):
        for j in range(len(parameters)):
          param = parameters[j]
          vmin  = param.get_pxd().priorModel.min
          vmax  = param.get_pxd().priorModel.max
          value = ests[i,j]
          value = vmin + value * (vmax-vmin)
          sample.get_estimates(param)[0].value = value
        if np.all([constraint.fn(sample) for constraint in constraints]):
          print 'parameter set %i of %i meets constraints' % (i+1,len(ests))
          good += [i]
        else:
          print 'parameter set %i of %i does not meet constraints' % (i+1,len(ests))
    else: good = range(len(ests))
    ests = ests[good,:]
    misc = {}
    misc['ests']={}
    for i in range(ests.shape[0]):
      misc['ests'][int(i)]={}
      for j in range(ests.shape[1]):
        misc['ests'][int(i)][int(parameters[j].id)] = ests[i,j]
    misc['i'] = int(0)
    self.misc = misc
#    self.misc = pickle.dumps(self.misc)
#    self.misc = json.dumps(self.misc)
    session = sqlalchemy.inspect(self).session
    for estimate in sample.estimates: session.delete(estimate)
    session.delete(sample)
    session.flush()
    session.commit()
    print len(good), len(ests)

  def presample(self,args=None): return []

  def generate_sample(self,misc,args=None,runLocal=False):
    t0=time.time()
    misc = self.misc
#    for key,value in misc['ests'].iteritems():
#      print key, type(key)
#    misc = pickle.loads(self.misc)
#    misc = json.loads(self.misc)
#    print 'loading', time.time()-t0
#    t0=time.time()
    if int(misc['i'])>=len(misc['ests']): return []
    sample = Sample(optimization=self)
    self.setup_simulations(sample)
    constraints = self.get_constraints()
    parameters = self.parameters
#    print 'misc', time.time()-t0
#    t0=time.time()
    for j in range(len(parameters)):
      param = parameters[j]
      vmin  = param.get_pxd().priorModel.min
      vmax  = param.get_pxd().priorModel.max
#      print misc['ests'][unicode(misc['i'])]
#      print misc['ests'][unicode(misc['i'])][unicode(param.id)]
      value = misc['ests'][unicode(misc['i'])][unicode(param.id)]
      value = vmin + value * (vmax-vmin)
#      print param.property.title, param.structure.domain.title, value
      estimate = Estimate(sample=sample,parameter=param,value=value)
      param.estimates.append(estimate)
#    print 'assigning values', time.time()-t0
    misc['i']=unicode(int(misc['i'])+1)
#    t0=time.time()
    sample.push(runLocal)
#    print 'pushing', time.time()-t0
    self.misc = misc
#    t0=time.time()
#    self.misc = json.dumps(misc)
#    self.misc = pickle.dumps(misc)
    print 'complete', time.time()-t0
    return [sample]
