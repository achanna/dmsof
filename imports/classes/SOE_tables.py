import sys
sys.path.append('../misc')
from header import *

def start_bucket(aws_id,aws_key,bucket):
  s3 = S3Connection( aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
  try:    b = s3.get_bucket(bucket)
  except: b = s3.create_bucket(bucket)
  if b==None: s3.create_bucket(bucket)
  else:
    for k in b.list():
      print 'deleting', k
      k.delete()
  sqs = boto.sqs.connect_to_region('us-west-2', aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
  q  = sqs.get_queue('%s_input' % bucket )
  if q==None: sqs.create_queue('%s_input' % bucket )
  else: q.clear()
  q   = sqs.get_queue('%s_start' % bucket )
  if q==None: sqs.create_queue('%s_start' % bucket )
  else: q.clear()
  q   = sqs.get_queue('%s_output' % bucket )
  if q==None: sqs.create_queue('%s_output' % bucket )
  else: q.clear()

def pareto_rank_old(samples,domrel):

  t0 = time.time()
  sys.stdout.write('starting pareto sorting...\n')
  sys.stdout.flush()

  currentRank=1
  paretoRank  = {}
  for sample in samples: paretoRank[sample.id] = currentRank

  ii=range(len(samples))
  out=[]

  while True:

    print 'Checking %i samples for rank %i condition...' % (len(ii)-len(out),currentRank)

    finished=1
    for i in ii:
      if i in out: continue
      for j in ii:
        if i==j: continue
        if j in out: continue
        if domrel[j,i]:
          paretoRank[samples[i].id] += 1
          finished=0
          break

    for i in ii:
      if paretoRank[samples[i].id]==currentRank: out += [i]

    if finished: break
    currentRank+=1

  sys.stdout.write('complete [t=%f seconds]\n' % (time.time()-t0) )
  sys.stdout.flush()
  return paretoRank

def pareto_rank(samples,domrel):

  t0 = time.time()
  sys.stdout.write('starting pareto sorting...\n')
  sys.stdout.flush()

  currentRank=1
  ids={}
  paretoRank={}

  for i in range(len(samples)):
    paretoRank[samples[i].id] = currentRank
    ids[samples[i].id] = i

  ii=range(len(samples))

  while True:

    avail=0
    for i in ii:
      if paretoRank[samples[i].id]==currentRank:
        avail+=1
    print 'Checking %i samples for rank %i condition...' % (avail,currentRank)

    finished=1
    for i in ii:
      for j in ii:
        if i==j: continue
        if domrel[j,i] and paretoRank[samples[i].id]==currentRank and paretoRank[samples[j].id]==currentRank:
          paretoRank[samples[i].id] += 1
          finished=0
          break

    if finished: break
    currentRank+=1
    if currentRank>=30: break

  sys.stdout.write('complete [t=%f seconds]\n' % (time.time()-t0) )
  sys.stdout.flush()
  return paretoRank

def compute_pareto_ranks(opts, objs=None, save=True):

  t0 = time.time()
  sys.stdout.write('forming list of complete samples...')
  sys.stdout.flush()

  if type(objs)==type(None):
    session = sqlalchemy.inspect(opts[0]).session
    objs    = session.query(Objective).all()

  samples=[]
  for opt in opts:
    for sample in opt.samples:
      if sample.status()==2:
        samples.append(sample)

  sys.stdout.write('complete [t=%f seconds]\n' % (time.time()-t0) )
  sys.stdout.flush()

  ids=[]
  for sample in samples: ids += [sample.id]
  nn=len(ids)

  t0 = time.time()
  sys.stdout.write('collecting error values...')
  sys.stdout.flush()
  errs = np.zeros([nn,len(objs)],dtype='float')
  for i in range(nn):
    errs[i,:] = samples[i].get_errors(objs)
  sys.stdout.write('complete [t=%f seconds]\n' % (time.time()-t0) )
  sys.stdout.flush()


  if save: pickle.dump({'ids':ids,'errs':errs,'paretoRank':paretoRank},open('pareto.pkl','wb'))
  return paretoRank

def start_pareto_rank_structure(opts, objs=None, save=True):

  t0 = time.time()
  sys.stdout.write('forming list of complete samples...')
  sys.stdout.flush()

  if type(objs)==type(None):
    session = sqlalchemy.inspect(opts[0]).session
    objs    = session.query(Objective).all()

  if isinstance(opts[0],Optimization):
    samples=[]
    for opt in opts:
      for sample in opt.samples:
        if sample.status()==2:
          samples.append(sample)
  else:
    samples = opts

  sys.stdout.write('complete [t=%f seconds]\n' % (time.time()-t0) )
  sys.stdout.flush()

  ids=[]
  for sample in samples: ids += [sample.id]
  nn=len(ids)

  t0 = time.time()
  sys.stdout.write('collecting error values...')
  sys.stdout.flush()
  errs = np.zeros([nn,len(objs)],dtype='float')
  for i in range(nn):
    errs[i,:] = samples[i].get_errors(objs)
  sys.stdout.write('complete [t=%f seconds]\n' % (time.time()-t0) )
  sys.stdout.flush()

#    print i, nn
#  pickle.dump(errs,open('./errs.pkl','wb'))
#  exit()

  t0 = time.time()
  sys.stdout.write('starting pareto relationships...')
  sys.stdout.flush()
  domrel = np.zeros([nn,nn],dtype='bool')

#  for i,j in list(itertools.permutations(range(nn),2)):
  for i in range(nn):
    for j in range(nn):
      if i==j: domrel[i,j]=False
      else:
        le = np.less_equal(errs[i,:],errs[j,:])
        lt = np.less(errs[i,:],errs[j,:])
        domrel[i,j] = np.all(le) and np.any(lt)
  sys.stdout.write('complete [t=%f seconds]\n' % (time.time()-t0) )
  sys.stdout.flush()

  paretoRank = pareto_rank(samples,domrel)
  #if save: pickle.dump({'ids':ids,'errs':errs,'domrel':domrel,'paretoRank':paretoRank},open('pareto.pkl','wb'))
  if save: pickle.dump({'ids':ids,'errs':0,'domrel':0,'paretoRank':paretoRank},open('pareto.pkl','wb'))
  return paretoRank

def update_pareto_rank_structure(opts, objs=None, save=True):

  file = pickle.load(open('pareto.pkl','rb'))
  old_ids        = file['ids']
  old_errs       = file['errs']
  old_domrel     = file['domrel']
  old_paretoRank = file['paretoRank']

  t0 = time.time()
  sys.stdout.write('forming list of complete samples...')
  sys.stdout.flush()

  if type(objs)==type(None):
    session = sqlalchemy.inspect(opts[0]).session
    objs    = session.query(Objective).all()

  samples=[]
  for opt in opts:
    for sample in opt.samples:
      if sample.status()==2:
        samples.append(sample)

  sys.stdout.write('complete [t=%f seconds]\n' % (time.time()-t0) )
  sys.stdout.flush()

  ids=[]
  for sample in samples: ids += [sample.id]
  new_ids = list(set(ids)-set(old_ids))
  ii = np.where(np.in1d(ids,new_ids))[0]

  t0 = time.time()
  sys.stdout.write('collecting error values...')
  sys.stdout.flush()
  errs = old_errs.copy()
  for i in ii:
    errs = np.vstack([ errs, samples[i].get_errors(objs) ])
  sys.stdout.write('complete [t=%f seconds]\n' % (time.time()-t0) )
  sys.stdout.flush()

  t0 = time.time()
  sys.stdout.write('starting pareto relationships...')
  sys.stdout.flush()
  domrel = old_domrel.copy()
  for isamp in ii:
    domrel = np.hstack([domrel,np.zeros([domrel.shape[0],1],dtype='float')])
    domrel = np.vstack([domrel,np.zeros([1,domrel.shape[1]],dtype='float')])
    j=domrel.shape[1]-1
    for i in range(domrel.shape[0]):
      if i==j: domrel[i,j]=False
      else:
        le = np.less_equal(errs[i,:],errs[j,:])
        lt = np.less(errs[i,:],errs[j,:])
        domrel[i,j] = np.all(le) and np.any(lt)
    i=domrel.shape[0]-1
    for j in range(domrel.shape[1]-1):
      if i==j: domrel[i,j]=False
      else:
        le = np.less_equal(errs[i,:],errs[j,:])
        lt = np.less(errs[i,:],errs[j,:])
        domrel[i,j] = np.all(le) and np.any(lt)
  sys.stdout.write('complete [t=%f seconds]\n' % (time.time()-t0) )
  sys.stdout.flush()

  paretoRank = pareto_rank(samples,domrel)
  if save: pickle.dump({'ids':ids,'errs':errs,'domrel':domrel,'paretoRank':paretoRank},open('pareto.pkl','wb'))
  return paretoRank

def find_parameters(opts):
  parameters=[]
  for opt in opts:
    parameters += opt.parameters
  return list(set(parameters))

Base = declarative_base()

prop_x_constraint = Table('prop_x_constraint', Base.metadata,
    Column('prop_id',       Integer, ForeignKey('property.id')),
    Column('constraint_id', Integer, ForeignKey('constraint.id')))

pxd_x_constraint = Table('pxd_x_constraint', Base.metadata,
    Column('pxd_id',        Integer, ForeignKey('pxd.id')),
    Column('constraint_id', Integer, ForeignKey('constraint.id')))

parameter_x_optimization = Table('parameter_x_optimization', Base.metadata,
    Column('parameter_id',    Integer, ForeignKey('parameter.id')),
    Column('optimization_id', Integer, ForeignKey('optimization.id')))

pxd_x_optimization = Table('pxd_x_optimization', Base.metadata,
    Column('pxd_id',          Integer, ForeignKey('pxd.id')),
    Column('optimization_id', Integer, ForeignKey('optimization.id')))

objective_x_optimization = Table('objective_x_optimization', Base.metadata,
    Column('objective_id',    Integer, ForeignKey('objective.id')),
    Column('optimization_id', Integer, ForeignKey('optimization.id')))

strucMod_x_optimization = Table('strucMod_x_optimization', Base.metadata,
    Column('strucMod_id',     Integer, ForeignKey('structuralModel.id')),
    Column('optimization_id', Integer, ForeignKey('optimization.id')))

strucMod_x_pxd = Table('strucMod_x_pxd', Base.metadata,
    Column('strucMod_id', Integer, ForeignKey('structuralModel.id')),
    Column('pxd_id',      Integer, ForeignKey('pxd.id')))

meas_x_obj = Table('meas_x_obj', Base.metadata,
    Column('meas_id', Integer, ForeignKey('measurement.id')),
    Column('obj_id',  Integer, ForeignKey('objective.id')))

inst_x_meas = Table('inst_x_meas', Base.metadata,
    Column('inst_id', Integer, ForeignKey('instrument.id')),
    Column('meas_id', Integer, ForeignKey('measurement.id')))

class Property(Base):

  __tablename__ = 'property'
  id            = Column(Integer, primary_key=True)
  title         = Column(String(64))
  abv           = Column(String(64))
  unit          = Column(String(64))
  pxds          = relationship( 'Prop_X_Domain',  back_populates='property' )
  parameters    = relationship( 'Parameter',      back_populates='property' )
  constraints   = relationship( 'Constraint',     back_populates='properties', secondary=prop_x_constraint )

class Domain(Base):

  __tablename__   = 'domain'
  id              = Column(Integer, primary_key=True)
  title           = Column(String(64))
  geom            = Column(PickleType)
  pxds            = relationship( 'Prop_X_Domain',   back_populates='domain')
  structures      = relationship( 'Structure',       back_populates='domain')
  heterogeneities = relationship( 'Heterogeneity',   back_populates='domain')

  def generate_geometry(self):
    nd = self.geom.shape[0]
    geom = np.zeros([nd],dtype='float')
    for id in range(nd):
      vmin = self.geom[id,0]
      vmax = self.geom[id,1]
      geom[id] = np.random.uniform(vmin,vmax)
    return geom

class Heterogeneity(Base):

  __tablename__   = 'heterogeneity'
  id_domain       = Column(Integer, ForeignKey('domain.id'),       primary_key=True )
  id_optimization = Column(Integer, ForeignKey('optimization.id'), primary_key=True )
  spatial         = Column(PickleType)
  temporal        = Column(PickleType)
  domain          = relationship('Domain',       back_populates='heterogeneities' )
  optimization    = relationship('Optimization', back_populates='heterogeneities' )

class StructuralModel(Base):

  __tablename__ = 'structuralModel'
  id            = Column(Integer, primary_key=True )
  model         = Column(PickleType)
  optimizations = relationship( 'Optimization',  back_populates='strucMods', secondary=strucMod_x_optimization )
  pxds          = relationship( 'Prop_X_Domain', back_populates='strucMods', secondary=strucMod_x_pxd )

class Prop_X_Domain(Base):

  __tablename__ = 'pxd'
  id            = Column(Integer, primary_key=True)
  id_property   = Column(Integer, ForeignKey('property.id'), primary_key=True )
  id_domain     = Column(Integer, ForeignKey('domain.id'),   primary_key=True )
  priorModel    = Column(PickleType)
  property      = relationship( 'Property',        back_populates='pxds' )
  domain        = relationship( 'Domain',          back_populates='pxds' )
  constraints   = relationship( 'Constraint',      back_populates='pxds', secondary=pxd_x_constraint )
  optimizations = relationship( 'Optimization',    back_populates='pxds', secondary=pxd_x_optimization )
  strucMods     = relationship( 'StructuralModel', back_populates='pxds', secondary=strucMod_x_pxd )

class Constraint(Base):

  __tablename__ = 'constraint'
  id            = Column(Integer, primary_key=True)
  fn            = Column(PickleType)
  properties    = relationship('Property',      back_populates='constraints', secondary=prop_x_constraint )
  pxds          = relationship('Prop_X_Domain', back_populates='constraints', secondary=pxd_x_constraint  )

class Structure(Base):

  __tablename__ ='structure'
  id            = Column(Integer, primary_key=True)
  id_domain     = Column(Integer, ForeignKey('domain.id'),   primary_key=True )
  geom          = Column(PickleType)
  domain        = relationship( 'Domain',    back_populates='structures' )
  parameters    = relationship( 'Parameter', back_populates='structure'  )

class Parameter(Base):

  __tablename__ = 'parameter'
  id            = Column(Integer, primary_key=True)
  id_property   = Column(Integer, ForeignKey('property.id'),  primary_key=True )
  id_structure  = Column(Integer, ForeignKey('structure.id'), primary_key=True )
  property      = relationship( 'Property',     back_populates='parameters' )
  structure     = relationship( 'Structure',    back_populates='parameters' )
  estimates     = relationship( 'Estimate',     back_populates='parameter'  )
  optimizations = relationship( 'Optimization', back_populates='parameters', secondary=parameter_x_optimization )

  def get_pxd(self):
    prop = self.property
    strc = self.structure
    domn = strc.domain
    return list(set(domn.pxds).intersection(set(prop.pxds)))[0]

class Estimate(Base):

  __tablename__ = 'estimate'
  id            = Column(Integer, primary_key=True)
  id_sample     = Column(Integer, ForeignKey('sample.id'),    primary_key=True )
  id_parameter  = Column(Integer, ForeignKey('parameter.id'), primary_key=True )
  value         = Column(Float)
  sample        = relationship( 'Sample',    back_populates='estimates' )
  parameter     = relationship( 'Parameter', back_populates='estimates' )

class InstrumentType(Base):

  __tablename__ = 'instrumentType'
  id            = Column(Integer, primary_key=True)
  title         = Column(String(64))
  abv           = Column(String(64))
  unit          = Column(String(64))
  instruments   = relationship( 'Instrument', back_populates='instType' )

class Instrument(Base):

  __tablename__ = 'instrument'
  id            = Column(Integer, primary_key=True)
  id_instType   = Column(Integer, ForeignKey('instrumentType.id'), primary_key=True )
  title         = Column(String(64))
  geom          = Column(PickleType)
  instType      = relationship( 'InstrumentType', back_populates='instruments' )
  measurements  = relationship( 'Measurement',    back_populates='instruments', secondary=inst_x_meas )

class ForwardModel(Base):

  __tablename__ = 'forwardModel'
  id            = Column(Integer, primary_key=True)
  title         = Column(String(64))
  fmod          = Column(PickleType)
  simulations   = relationship( 'Simulation', back_populates='forwardModel' )
  signalTypes   = relationship( 'SignalType', back_populates='forwardModel' )

class Measurement(Base):

  __tablename__      = 'measurement'
  id                 = Column(Integer, primary_key=True)
  indVars_prescribed = Column(PickleType)
  indVars_actual     = Column(PickleType)
  data               = Column(PickleType)
  sigsq              = Column(Float)
  weight             = Column(Float)
  detrend            = Column(PickleType)
  instruments        = relationship( 'Instrument', back_populates='measurements', secondary=inst_x_meas )
  objectives         = relationship( 'Objective',  back_populates='measurements', secondary=meas_x_obj  )
  signalTypes        = relationship( 'SignalType', back_populates='measurement' )
  predictions        = relationship( 'Prediction', back_populates='measurement' )

class SignalType(Base):

  __tablename__ = 'signalType'
  id             = Column(Integer, primary_key=True )
  id_forwardMod  = Column(Integer, ForeignKey('forwardModel.id') )
  id_measurement = Column(Integer, ForeignKey('measurement.id') )
  signals        = relationship( 'Signal',       back_populates='signalType' )
  forwardModel   = relationship( 'ForwardModel', back_populates='signalTypes' )
  measurement    = relationship( 'Measurement',  back_populates='signalTypes' )

class Signal(Base):

  __tablename__ = 'signal'
  id_signalType = Column(Integer, ForeignKey('signalType.id'), primary_key=True )
  id_simulation = Column(Integer, ForeignKey('simulation.id'), primary_key=True )
  id_prediction = Column(Integer, ForeignKey('prediction.id'), primary_key=True )
  data          = Column(PickleType)
  signalType    = relationship( 'SignalType', back_populates='signals' )
  simulation    = relationship( 'Simulation', back_populates='signals' )
  prediction    = relationship( 'Prediction', back_populates='signals' )

class Objective(Base):

  __tablename__   = 'objective'
  id              = Column(Integer, primary_key=True)
  post            = Column(PickleType,default=None)
  measurements    = relationship( 'Measurement',  back_populates='objectives', secondary=meas_x_obj )
  optimizations   = relationship( 'Optimization', back_populates='objectives', secondary=objective_x_optimization )

class Prediction(Base):

  __tablename__ = 'prediction'
  id            = Column(Integer, primary_key=True)
  id_sample     = Column(Integer, ForeignKey('sample.id'), primary_key=True )
  id_meas       = Column(Integer, ForeignKey('measurement.id'), primary_key=True )
  data          = Column(PickleType,default=None)
  misfit        = Column(Float,default=None)
  misfitFresh   = Column(Boolean,default=False)
  sample        = relationship( 'Sample',      back_populates='predictions' )
  measurement   = relationship( 'Measurement', back_populates='predictions' )
  signals       = relationship( 'Signal',      back_populates='prediction' )

  def fetch_misfit(self,needFresh=True):
    if self.misfitFresh and needFresh: return self.misfit
    if (self.misfit)!=type(None) and not needFresh: return self.misfit
    if type(self.data)==type(None) or np.any(np.isnan(self.data)):
      self.misfit = None
      return None
    if type(self.measurement.data)==type(None):
      self.misfit = None
      return None
    indV_pred,data_pred = self.measurement.detrend(self)
#    print data_pred
    if self.measurement.data.ndim==2:
      indV_meas           = self.measurement.data[:,0]
      data_meas           = self.measurement.data[:,1]
      data_pred_i         = np.interp(indV_meas,indV_pred,data_pred)
#      misfit              = np.std(data_pred_i-data_meas)
      misfit              = np.sum((data_pred_i-data_meas)**2)**0.5/float(len(data_meas))**0.5
    else:
      misfit = np.sum((self.measurement.data-data_pred)**2)**0.5
    if np.isnan(misfit) or misfit>1e10:
      self.misfit = None
      return None
    else:
      self.misfit         = misfit
      self.misfitFresh    = True
      return self.misfit

class Simulation(Base):

  __tablename__       = 'simulation'
  id                  = Column(Integer, primary_key=True)
  id_sample           = Column(Integer, ForeignKey('sample.id'), primary_key=True )
  id_forwardModel     = Column(Integer, ForeignKey('forwardModel.id'), primary_key=True )
  inputFilePushed     = Column(Boolean,default=False)
  inputFileTime       = Column(DateTime)
  outputFileStartTime = Column(DateTime)
  outputFileEndTime   = Column(DateTime)
  output              = Column(PickleType)
  sample              = relationship( 'Sample',       back_populates='simulations' )
  forwardModel        = relationship( 'ForwardModel', back_populates='simulations' )
  signals             = relationship( 'Signal',       back_populates='simulation'  )

  def push(self,runLocal=False):
    print self
    model = {}
    model['estimates']={}
    model['misc']=self.sample.misc
    for estimate in self.sample.estimates:
      model['estimates'][estimate.id]={}
      model['estimates'][estimate.id]['abv']    = estimate.parameter.property.abv
      model['estimates'][estimate.id]['geom']   = estimate.parameter.structure.geom
      model['estimates'][estimate.id]['domain'] = estimate.parameter.structure.domain.title
      model['estimates'][estimate.id]['value']  = estimate.value
    model['signals']={}
    for signal in self.signals:
      model['signals'][signal.id_signalType]={}
      model['signals'][signal.id_signalType]['indVars'] = signal.prediction.measurement.indVars_prescribed
      model['signals'][signal.id_signalType]['instruments']={}
      for instrument in signal.prediction.measurement.instruments:
        model['signals'][signal.id_signalType]['instruments'][instrument.id]={}
        model['signals'][signal.id_signalType]['instruments'][instrument.id]['abv']  = instrument.instType.abv
        model['signals'][signal.id_signalType]['instruments'][instrument.id]['geom'] = instrument.geom
    if runLocal==False:
      self.forwardModel.fmod(model)
      s3  = S3Connection( aws_access_key_id=self.sample.optimization.aws_id, aws_secret_access_key=self.sample.optimization.aws_key )
      sqs = boto.sqs.connect_to_region("us-west-2", aws_access_key_id=self.sample.optimization.aws_id, aws_secret_access_key=self.sample.optimization.aws_key)
      b = s3.get_bucket(self.sample.optimization.bucket)
      q = sqs.get_queue('%s_input' % self.sample.optimization.bucket)
      k = Key(b)
      m = Message(q)
      k.key = 'input_%i' % self.id
      k.set_contents_from_filename('input-files.tgz')
      m.set_body('%i' % self.id)
      q.write(m)
      s3.close()
      self.inputFilePushed = True
      self.inputFileTime   = datetime.datetime.utcnow()
    else:
      self.forwardModel.fmod(model)
      self.inputFilePushed = True
      self.inputFileTime   = datetime.datetime.utcnow()
      runLocal()
      output = pickle.load(open('output.pkl','rb'))
      times  = output['times']
      output = output['output']
      simulation = self.sample.optimization.get_simulation(self.id)
      self.outputFileStartTime = times[0]
      self.outputFileEndTime   = times[1]
      self.output = 'output_%i' % self.id
      for signal in self.signals:
        for id_signalType,data in output.iteritems():
          if id_signalType==signal.id_signalType:
            signal.data = data
            signal.prediction.data = data

class Sample(Base):

  __tablename__   = 'sample'
  id              = Column(Integer, primary_key=True)
  id_optimization = Column(Integer, ForeignKey('optimization.id'), primary_key=True )
  misc            = Column(PickleType)
  statusInt       = Column(Integer,default=0)
  simulations     = relationship( 'Simulation',   back_populates='sample' )
  estimates       = relationship( 'Estimate',     back_populates='sample' )
  predictions     = relationship( 'Prediction',   back_populates='sample' )
  optimization    = relationship( 'Optimization', back_populates='samples' )

  def is_within_bounds(self):
    for estimate in self.estimates:
      min = estimate.parameter.get_pxd().priorModel.min
      max = estimate.parameter.get_pxd().priorModel.max
      if estimate.value<min: return False
      if estimate.value>max: return False
    return True

  def subj_relates(self):
    relates = []
    for relate in self.optimization.relations:
      if relate.sample_subj==self: relates.append(relate)
    return relates

  def obj_relates(self):
    relates = []
    for relate in self.optimization.relations:
      if relate.sample_obj==self: relates.append(relate)
    return relates

  def get_estimates(self,parameter):
    estimates=[]
    for estimate in self.estimates:
      if estimate.parameter==parameter:
        estimates.append( estimate )
    return estimates

  def get_predictions(self,objective):
    predictions=[]
    for simulation in self.simulations:
      for signal in simulation.signals:
        if objective in signal.prediction.measurement.objectives:
          predictions += [ signal.prediction ]
    return list(set(predictions))

  def get_parameters(self):
    parameters = []
    for estimate in self.estimates:
      parameters.append( estimate.parameter )
    return parameters

  def get_weighted_error(self):
    error=0
    for simulation in self.simulations:
      for prediction in simulation.predictions:
        error += prediction.fetch_misfit() / prediction.objective.measurement.sigsq**0.5
    return error

  def get_errors(self,objs=None):
    if type(objs)==type(None): objs = self.optimization.objectives
    else: objs = objs
    errors=[]
    for obj in objs:
      for prediction in self.get_predictions(obj):
        errors.append( prediction.fetch_misfit() )
    return np.array(errors)

  def likelihood_unnormalized(self):
    likelihood = 1
    preds=[]
    for simulation in self.simulations:
      for signal in simulation.signals:
        preds += [signal.prediction]
    for prediction in list(set(preds)):
      sigsq = prediction.measurement.sigsq
      misfit = prediction.misfit
      li = (2*math.pi*sigsq)**-0.5 * np.exp( -misfit**2 / (2*sigsq**2) )
      li = misfit
      likelihood *= li
    return likelihood

  def status(self):
    # not ready to run = 0
    if self.statusInt==2: return 2
    for simulation in self.simulations:
      if simulation.inputFilePushed==False: return 0
    # ready to run, not completed = 1
    for simulation in self.simulations:
      for signal in simulation.signals:
        if type(signal.data)==type(None): return 1.1
        if not all( isinstance(datum, float) for datum in signal.data): return 1.2
        if signal.prediction.fetch_misfit()==None: return 1.3
    if len(self.get_errors())==0: return 1.4
    # completed = 2
    self.statusInt = 2
    return 2

  def copy(self):
    copy = Sample(optimization=self.optimization)
    self.optimization.setup_simulations(copy)
    for estimate in self.estimates:
      newEst = Estimate(sample=copy,parameter=estimate.parameter,value=estimate.value)
      estimate.parameter.estimates.append(newEst)
    copy.misc = self.misc.copy()
    return copy

  def interp_model_to_grid(self,XY):
    rho = []
    for estimate in self.estimates:
      rho.append( estimate.value )
    ell1 = matplotlib.patches.Ellipse( (+40,-30), +20, +40, +60 )
    ell2 = matplotlib.patches.Ellipse( (-30,-20), +18, +60, -15 )
    x = np.linspace(-100,100,200)
    y = np.linspace(0,-100,100)
    X,Y = np.meshgrid(x,y)
    D = np.zeros(X.shape)
    for i in range(X.shape[0]):
      for j in range(X.shape[1]):
        ix = X[i,j]
        iy = Y[i,j]
        if   ell1.contains_point((ix,iy)): D[i,j] = rho[1]
        elif ell2.contains_point((ix,iy)): D[i,j] = rho[2]
        else: D[i,j] = rho[0]
    return D

  def push(self,runLocal=False):
    t0=time.time()
    session = sqlalchemy.inspect(self).session
    session.commit()
    for simulation in self.simulations:
      simulation.push(runLocal)

class Relate(Base):

  __tablename__   = 'relate'
  id              = Column(Integer, primary_key=True)
  id_optimization = Column(Integer, ForeignKey('optimization.id') )
  id_subject      = Column(Integer, ForeignKey('sample.id') )
  id_object       = Column(Integer, ForeignKey('sample.id') )
  relation        = Column(Enum('proposed','accepted','rejected','parent','antecedent','neighbor','dominates','killed'))
  optimization    = relationship( 'Optimization', back_populates='relations' )
  sample_subj     = relationship( 'Sample', foreign_keys=[id_subject] )
  sample_obj      = relationship( 'Sample', foreign_keys=[id_object]  )

class Optimization(Base):

  __tablename__   = 'optimization'
  id              = Column(Integer, primary_key=True)
  type            = Column(String(64))
  aws_id          = Column(String(64))
  aws_key         = Column(String(64))
  bucket          = Column(String(64))
#  misc            = Column(LargeBinary)
#  misc            = Column(PickleType(pickler=json))
  misc            = Column( sqlalchemy.ext.mutable.MutableDict.as_mutable(PickleType(pickler=json)) )
  samples         = relationship( 'Sample',          back_populates='optimization' )
  relations       = relationship( 'Relate',          back_populates='optimization' )
  heterogeneities = relationship( 'Heterogeneity',   back_populates='optimization' )
  parameters      = relationship( 'Parameter',       back_populates='optimizations', secondary=parameter_x_optimization )
  strucMods       = relationship( 'StructuralModel', back_populates='optimizations', secondary=strucMod_x_optimization  )
  pxds            = relationship( 'Prop_X_Domain',   back_populates='optimizations', secondary=pxd_x_optimization       )
  objectives      = relationship( 'Objective',       back_populates='optimizations', secondary=objective_x_optimization )
  __mapper_args__ = { 'polymorphic_on':type, 'polymorphic_identity':'optimization' }

  def push_all(self,ids):
    for sample in self.get_complete_samples():
      if sample.id in ids:
        sample.push()

  def random_parameterization(self):
    params=[]
    for domain in self.get_domains():
      hets = list(set(self.heterogeneities).intersection(domain.heterogeneities))
      if len(hets)==1: nStrucs=np.random.randint(hets[0].spatial[0],hets[0].spatial[1])
      else:            nStrucs = 1
      for ii in range(nStrucs):
        geom  = domain.generate_geometry()
        struc = Structure( domain=domain, geom=geom )
        for pxd in domain.pxds:
          params.append( Parameter(structure=struc,property=pxd.property) )
    return params

  def grid_parameterization(self,nDims):
    params=[]
    for domain in self.get_domains():
      x = np.linspace(domain.geom[0,0],domain.geom[0,1],nDims[0])
      y = np.linspace(domain.geom[1,0],domain.geom[1,1],nDims[1])
      X,Y = np.meshgrid(x,y)
      x=X.ravel()
      y=Y.ravel()
      for i in range(len(x)):
        geom  = np.array([x[i],y[i]])
        struc = Structure( domain=domain, geom=geom )
        for pxd in domain.pxds:
          params.append( Parameter(structure=struc,property=pxd.property) )
    return params

  def get_parameters(self):
    if len(self.parameters)>0: return self.parameters
    else:                      return self.random_parameterization()

  def get_domains(self):
    domains=[]
    for pxd in self.pxds:
      domains.append( pxd.domain )
    return list(set(domains))

  def get_properties(self):
    properties=[]
    for pxd in self.pxds:
      properties.append( pxd.property )
    return list(set(properties))

  def get_forwardModels(self):
    fms=[]
    for objective in self.objectives:
      for measurement in objective.measurements:
        for sigType in measurement.signalTypes:
          fms += [sigType.forwardModel]
    return list(set(fms))

  def get_measurements(self):
    meas=[]
    for obj in self.objectives:
      for measurement in obj.measurements:
        meas += [measurement]
    return list(set(meas))

  def generate_samples(self,n,args=0,runLocal=False):
    outputs=[]
    args['n']=n
    misc = self.presample(args)
    for i in range(n):
      sys.stdout.write('Generating sample n=%i/%i (%i)...\n' % (i+1,n,len(self.samples)+1) )
      sys.stdout.flush()
      outputs += self.generate_sample(misc,args,runLocal)
    return outputs

  def push_input_files(self,aws_id,aws_key,bucket):
    for sample in self.samples:
      for simulation in sample.simulations:
        if not simulation.inputFilePushed:
          simulation.forwardModel.fmod(simulation,aws_id,aws_key,bucket)

  def setup_simulations(self,sample):
    for forwardModel in self.get_forwardModels():
      Simulation(sample=sample,forwardModel=forwardModel)
    for meas in self.get_measurements():
      pred = Prediction(sample=sample,measurement=meas)
      for sigType in meas.signalTypes:
        for sim in sample.simulations:
          if sigType.forwardModel==sim.forwardModel: break
        signal = Signal(signalType=sigType,simulation=sim,prediction=pred)

  def get_pushed_samples(self):
    session = sqlalchemy.inspect(self).session
    samples = session.query(Sample).all()
    pushed=[]
    for sample in samples:
      if np.all([simulation.inputFilePushed for simulation in sample.simulations]):
        pushed.append(sample)
    return pushed

  def retrieve_values(self):
    values = []
    for sample in self.samples:
      if np.all([simulation.inputFilePushed for simulation in sample.simulations]):
        values.append([estimate.value for estimate in sample.estimates])
    return values

  def normalizeEstimates(self,parameters,values):
    newVals = np.array(values).copy()
    for i in range(len(parameters)):
      prior = parameters[i].get_pxd().priorModel
      newVals[:,i] -= prior.min
      newVals[:,i] /= (prior.max-prior.min)
    return newVals

  def orderby(self,estimates,parameters):
    ordered=[]
    for parameter in parameter:
      for estimate in estimates:
        if estimate.parameter==parameter:
          ordered.append(estimate)
    return ordered

  def get_simulation(self,id_simulation):
    session = sqlalchemy.inspect(self).session
    return session.query(Simulation).filter_by(id=id_simulation).one()

  def retrieve_results(self,output_type=0):

    session = sqlalchemy.inspect(self).session
    session.commit()

    s3  = S3Connection( aws_access_key_id=self.aws_id, aws_secret_access_key=self.aws_key )
    sqs = boto.sqs.connect_to_region("us-west-2", aws_access_key_id=self.aws_id, aws_secret_access_key=self.aws_key)
    b   = s3.get_bucket(self.bucket)
    q   = sqs.get_queue('%s_output' % self.bucket)
    while True:
      t0 = time.time()
      sys.stdout.write('...checking for new output messages...')
      sys.stdout.flush()
      m = q.read(300)
      if m==None:
        sys.stdout.write('none found [%f s]\n' % (time.time()-t0))
        sys.stdout.flush()
        break
      sys.stdout.write('message found [%f s]\n' % (time.time()-t0))
      sys.stdout.flush()

      sys.stdout.write('...reading message')
      sys.stdout.flush()
      id_simulation = int(m.get_body())
      sys.stdout.write(' (id_simulation=%i)\n' % id_simulation)
      sys.stdout.flush()

      k = b.get_key('output_%i' % id_simulation )
      if k==None: break
      t0 = time.time()
      sys.stdout.write('...downloading output file from AWS\n')
      sys.stdout.flush()
      k.get_contents_to_filename('output.pkl')
      sys.stdout.write('...complete [%f s]\n' % (time.time()-t0))
      sys.stdout.flush()
#      os.system('tar xvzf output-files.tgz')

      if output_type==0:
        try:
          output = pickle.load(open('output.pkl','rb'))
          times  = output['times']
          output = output['output']

          simulation = self.get_simulation(id_simulation)
          simulation.outputFileStartTime = times[0]
          simulation.outputFileEndTime   = times[1]
          simulation.output = 'output_%i' % id_simulation

          for signal in simulation.signals:
            for id_signalType,data in output.iteritems():
              if id_signalType==signal.id_signalType:
                signal.data = data
        except: print 'whatevs'
      if output_type==1:
        os.system( 'cp output.pkl output_%07i.pkl' % id_simulation )
        simulation = self.get_simulation(id_simulation)
        simulation.output = 'output_%07i.pkl' % id_simulation

      q.delete_message(m)
      session.commit()

  def repost_broken_samples(self,runLocal=False):
    s3  = S3Connection( aws_access_key_id=self.aws_id, aws_secret_access_key=self.aws_key )
    sqs = boto.sqs.connect_to_region("us-west-2", aws_access_key_id=self.aws_id, aws_secret_access_key=self.aws_key)
    b   = s3.get_bucket(self.bucket)
    qi  = sqs.get_queue('%s_input' % self.bucket)
    qs  = sqs.get_queue('%s_start' % self.bucket)
    qo  = sqs.get_queue('%s_output' % self.bucket)

    sqs.purge_queue(qi)
    sqs.purge_queue(qs)
    sqs.purge_queue(qo)

    for key in b.get_all_keys(): key.delete()

    for sample in self.samples:
      for simulation in sample.simulations:
        if sample.status()!=2:
          if type(simulation.inputFileTime)!=type(None) and type(simulation.outputFileStartTime)==type(None):
            simulation.push(runLocal=False)
            print sample.id, simulation.id
            m = Message(qi)
            m.set_body('%i' % simulation.id)
            qi.write(m)

  def num_sims_unsimulated(self):
    n=0
    for sample in self.samples:
      for simulation in sample.simulations:
        if type(simulation.output)==type(None): n+=1
    return n

  def num_sims(self):
    n=0
    for sample in self.samples:
      for simulation in sample.simulations:
        n+=1
    return n

  def num_unsimulated(self):
    n = 0
    for sample in self.samples:
      if sample.status()==1:
        n+=1
    return n

  def num_simulated(self):
    n = 0
    for sample in self.samples:
      if sample.status()==2:
        n+=1
    return n

  def get_constraints(self):
    constraints=[]
    for pxd in self.pxds:
      for constraint in pxd.constraints:
        constraints.append(constraint)
    return list(set(constraints))

  def get_complete_samples(self):
    session = sqlalchemy.inspect(self).session
    samples = session.query(Sample).all()
    complete = []
    for sample in samples:
      if sample.status()==2:
        complete.append(sample)
    return complete

  def integrate_signals(self):
    for obj in self.objectives:
      for measurement in obj.measurements:
        for prediction in measurement.predictions:
          if type(prediction.data)==type(None):
            if not np.any([type(signal.data)==type(None) for signal in prediction.signals]):
              for signal in prediction.signals:
                if type(prediction.data)==type(None): prediction.data  = np.copy(signal.data)
                else:                                 prediction.data += signal.data
