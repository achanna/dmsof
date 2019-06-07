import sys
sys.path.append('/home/ubuntu/poroelast9/imports/misc')
from header import *
import pickle

import tradeoffs
import forwardModels
import postProcessors
import detrend
from connect_info import *

engine  = sqlalchemy.create_engine('mysql+mysqldb://%s:%s@localhost/%s'%(db_user,db_pswd,db_title), echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

opts = session.query(Optimization).all()
objs = session.query(Objective).all()

parameters = session.query(Parameter).all()

print objs[0].measurements[0].instruments[0].title
print objs[1].measurements[0].instruments[0].title
print objs[2].measurements[0].instruments[0].title
print objs[6].measurements[0].instruments[0].title
print objs[7].measurements[0].instruments[0].title
print objs[8].measurements[0].instruments[0].title

#exit()
#paretoRanks = start_pareto_rank_structure(opts,np.array(objs)[np.array([0,1,2,6,7,8])])

nPar=0
nErr=0
nBof=0

opts[1].misc['dead_ids']=[]
paretoRanks = pickle.load(open('pareto.pkl','rb'))['paretoRank']
samples = opts[0].get_complete_samples()
for sample in samples:
  exx = sample.get_predictions(objs[0])[0].fetch_misfit()
  eyy = sample.get_predictions(objs[1])[0].fetch_misfit()
  ezz = sample.get_predictions(objs[2])[0].fetch_misfit()

  pf1 = sample.get_predictions(objs[6])[0].fetch_misfit()
  pf2 = sample.get_predictions(objs[7])[0].fetch_misfit()
  pf3 = sample.get_predictions(objs[8])[0].fetch_misfit()

  bounds = [12,12,18,35,45,55]

  if paretoRanks[sample.id]==1: nPar+=1
  if (exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] and pf1<bounds[3] and pf2<bounds[4] and pf2<bounds[5]): nErr+=1
  if (exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] and pf1<bounds[3] and pf2<bounds[4] and pf2<bounds[5]) and paretoRanks[sample.id]==1: nBof+=1
  if (exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] and pf1<bounds[3] and pf2<bounds[4] and pf2<bounds[5]) and paretoRanks[sample.id]==1:
    print 'alive, sample %i', sample.id
  else:
    opts[1].misc['dead_ids'] += [sample.id]

print 'errs: %i, par: %i, both: %i' % (nErr,nPar,nBof)
#print opts[1].misc['dead_ids']
print len(opts[1].misc['dead_ids'])
print len(samples)

print len(samples)-len(opts[1].misc['dead_ids'])

session.add(opts[1])

session.commit()
