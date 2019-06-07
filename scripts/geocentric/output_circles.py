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
parameters = opts[0].parameters

paretoRanks = pickle.load(open('pareto.pkl','rb'))['paretoRank']
ests = []
for opt in opts:
  for sample in opt.samples:
    if sample.status()==2:

      exx = sample.get_predictions(objs[0])[0].fetch_misfit()
      eyy = sample.get_predictions(objs[1])[0].fetch_misfit()
      ezz = sample.get_predictions(objs[2])[0].fetch_misfit()

      pf1 = sample.get_predictions(objs[6])[0].fetch_misfit()
      pf2 = sample.get_predictions(objs[7])[0].fetch_misfit()
      pf3 = sample.get_predictions(objs[8])[0].fetch_misfit()

      bounds = [12,20,16,80,90,100]

      if True or (exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] and pf1<bounds[3] and pf2<bounds[4] and pf2<bounds[5]):

        for angle in [0]:
          sim = {}
          sim[1] = {}
          sim[2] = {}
          sim[3] = {}
          for parameter in parameters:
            if parameter.property.abv=='lr':
              sim[2][7] = sample.get_estimates(parameter)[0].value*2
              sim[2][8] = sample.get_estimates(parameter)[0].value*2
              sim[2][9] = angle
            else:
              sim[parameter.structure.domain.id][parameter.property.id] = sample.get_estimates(parameter)[0].value
          ests+=[sim]

params=[]
for param in parameters:
  params+=['%s %s'% (param.structure.domain.title,param.property.title)]

pickle.dump({'ests':ests,'params':params},open('circles.pkl','wb'))
