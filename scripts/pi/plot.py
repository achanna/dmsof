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

i=1
j=1
ptsIn  = []
ptsAll = []
for sample in opts[0].samples:
  x = sample.estimates[0].value
  y = sample.estimates[1].value
  r = (x**2+y**2)**0.5
  if r<1: j+=1
  ptsIn  += [j]
  ptsAll += [i]
  i+=1

ptsIn  = np.array(ptsIn,dtype='float')
ptsAll = np.array(ptsAll,dtype='float')

piEst  = np.divide(ptsIn,ptsAll)*4.0

plt.figure()
plt.plot( [0,10000], [np.pi,np.pi], 'r--', linewidth=2.0, zorder=0 )
plt.plot( range(len(piEst)), piEst, 'b', linewidth=2.0, zorder=1 )

plt.xlabel('Iterations',fontsize=28)
plt.ylabel('Estimate of $\pi$',fontsize=28)
plt.gca().set_xscale("log", nonposx='clip')
plt.xlim([1,10000])
plt.ylim([1,5])
plt.tick_params(axis='both', which='major', labelsize=20)
plt.savefig('pi_estimate.eps',format='eps',bbox_inches='tight')
plt.close()

session.commit()
