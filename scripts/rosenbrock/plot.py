#exit()

import sys
sys.path.append('/home/achanna/poroelast9/imports/misc')
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

plotting_codes.plot_pxd2d(opts,plotdir,'sims1')

session.commit()
