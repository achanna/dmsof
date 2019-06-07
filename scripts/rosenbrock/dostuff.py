import sys
sys.path.append('/home/achanna/Dropbox/poroelast8/imports/misc')
from header import *

import detrend
import tradeoffs
import likelihoods
import forwardModels
import postProcessors
from connect_info import *

t0=time.time()
engine  = sqlalchemy.create_engine('mysql+mysqldb://%s:%s@localhost/%s'%(db_user,db_pswd,db_title), echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#opts = session.query(Optimization).all()
#print len(opts)

#print len(session.query(Parameter).all())

#for meas in session.query(Measurement).all():
#  print meas.data

for prediction in session.query(Prediction).all():
  prediction.misfitFresh = False
session.commit()


#exit()

t=[]
eyy=[]
exx=[]
exy=[]
file=open('1a_shutin.txt')
for line in file:
  t.append(   line[:-1].split(',')[0] )
  eyy.append( line[:-1].split(',')[1] )
  exx.append( line[:-1].split(',')[2] )
  exy.append( line[:-1].split(',')[3] )

t   = np.array(t,dtype='float')
exx = np.array(exx,dtype='float')
eyy = np.array(eyy,dtype='float')
exy = np.array(exy,dtype='float')

I = np.where(np.multiply( 83<t, t<110  ))

t=t[I]
exx=+exx[I]
eyy=+eyy[I]
exy=-exy[I]

#t=t[I]
#exx=+eyy[I]
#eyy=+exx[I]
#exy=+exy[I]

t-=t[0]
eyy-=eyy[0]
exx-=exx[0]
exy-=exy[0]

exx*=1000
eyy*=1000
exy*=1000

exx-=4
eyy-=5
exy+=2

print np.min(t),   np.max(t)
print np.min(exx), np.max(exx)
print np.min(eyy), np.max(eyy)
print np.min(exy), np.max(exy)
#exit()

ntr  = 3500
tr   = np.linspace(np.min(t),np.max(t),ntr).reshape(ntr,1)
exxr = np.interp(tr,t,exx).reshape(ntr,1)
eyyr = np.interp(tr,t,eyy).reshape(ntr,1)
exyr = np.interp(tr,t,exy).reshape(ntr,1)

tr_exx = np.hstack((tr,exxr))
tr_eyy = np.hstack((tr,eyyr))
tr_exy = np.hstack((tr,exyr))

print tr_exx.shape

measurements = session.query(Measurement).all()
#for meas in measurements: meas.detrend = detrend.detrend

measurements[0].data=tr_exx
measurements[1].data=tr_eyy
measurements[2].data=tr_exy

#print measurements[0].objectives[0].instrument.title
#print measurements[1].objectives[0].instrument.title
#print measurements[2].objectives[0].instrument.title

session.commit()


