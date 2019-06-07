import sys
sys.path.append('/home/ubuntu/poroelast9/imports/misc')
from header import *

import detrend
import tradeoffs
import likelihoods
import forwardModels
import postProcessors
from connect_info import *

#print 'careful, stupid'
#exit(1)

con = MySQLdb.connect( db_addr, db_user, db_pswd )
cur = con.cursor()
cur.execute("DROP DATABASE IF EXISTS %s" % db_title)
con.commit()
cur.execute("CREATE DATABASE %s" % db_title)
cur.execute("USE %s" % db_title)
con.commit()
con.close()

start_bucket(aws_id,aws_key,bucket)

engine  = sqlalchemy.create_engine('mysql+mysqldb://%s:%s@localhost/%s'%(db_user,db_pswd,db_title), echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

con = MySQLdb.connect( db_addr, db_user, db_pswd )
cur = con.cursor()
cur.execute("USE %s" % db_title)
cur.execute("ALTER TABLE optimization MODIFY misc LONGBLOB")
con.commit()
con.close()

# define physical properties
properties=[]
properties.append( Property( title='Permeability',      abv='kappa', unit='m2'  ))
properties.append( Property( title='Bulk Modulus',      abv='K',     unit='GPa' ))
properties.append( Property( title='Porosity',          abv='phi',   unit='1' ))
properties.append( Property( title='Poisson Ratio',     abv='nu',    unit='1' ))

properties.append( Property( title='Centroid Easting',  abv='cx',    unit='m' ))
properties.append( Property( title='Centroid Northing', abv='cy',    unit='m' ))
properties.append( Property( title='Lens Radius',       abv='lr',    unit='m' ))
# define geometry and model domains
domains=[]
domains.append( Domain( title='Lens',      geom=np.array([[0,2000],[0,2000],[-250,+500]]) ))
domains.append( Domain( title='Formation', geom=np.array([[0,2000],[0,2000],[-250,+500]]) ))
domains.append( Domain( title='Confining', geom=np.array([[0,2000],[0,2000],[+500,+750]]) ))

# define prior probability distributions, define pxds

priorModel0  = Uniform(  -14.00,   -10.00,  0.050 )
priorModel1  = Uniform(    0.25,    20.00,  0.190 )
priorModel2  = Uniform(    0.02,     0.35,  0.190 )
priorModel3  = Uniform(    0.15,     0.35,  0.190 )

priorModel4  = Uniform( -800.00,  +800.00, 40.000 )
priorModel5  = Uniform( -800.00,  +800.00, 40.000 )
priorModel6  = Uniform(  +50.00, +1000.00,  7.000 )

priorModel7  = Uniform(  -16.00,   -12.00,  0.050 )
priorModel8  = Uniform(    0.25,    20.00,  0.190 )
priorModel9  = Uniform(    0.02,     0.35,  0.190 )
priorModel10 = Uniform(    0.15,     0.35,  0.190 )

priorModel11 = Uniform(  -18.00,   -13.00,  0.050 )
priorModel12 = Uniform(    0.25,    20.00,  0.190 )
priorModel13 = Uniform(    0.02,     0.35,  0.190 )
priorModel14 = Uniform(    0.15,     0.35,  0.190 )

pxds=[]
pxds.append( Prop_X_Domain( property=properties[0], domain=domains[0], priorModel=priorModel0 ))
pxds.append( Prop_X_Domain( property=properties[1], domain=domains[0], priorModel=priorModel1 ))
pxds.append( Prop_X_Domain( property=properties[2], domain=domains[0], priorModel=priorModel2 ))
pxds.append( Prop_X_Domain( property=properties[3], domain=domains[0], priorModel=priorModel3 ))

pxds.append( Prop_X_Domain( property=properties[4], domain=domains[0], priorModel=priorModel4 ))
pxds.append( Prop_X_Domain( property=properties[5], domain=domains[0], priorModel=priorModel5 ))
pxds.append( Prop_X_Domain( property=properties[6], domain=domains[0], priorModel=priorModel6 ))

pxds.append( Prop_X_Domain( property=properties[0], domain=domains[1], priorModel=priorModel7 ))
pxds.append( Prop_X_Domain( property=properties[1], domain=domains[1], priorModel=priorModel8 ))
pxds.append( Prop_X_Domain( property=properties[2], domain=domains[1], priorModel=priorModel9 ))
pxds.append( Prop_X_Domain( property=properties[3], domain=domains[1], priorModel=priorModel10 ))

pxds.append( Prop_X_Domain( property=properties[0], domain=domains[2], priorModel=priorModel11 ))
pxds.append( Prop_X_Domain( property=properties[1], domain=domains[2], priorModel=priorModel12 ))
pxds.append( Prop_X_Domain( property=properties[2], domain=domains[2], priorModel=priorModel13 ))
pxds.append( Prop_X_Domain( property=properties[3], domain=domains[2], priorModel=priorModel14 ))

constraints=[]
constraints.append(Constraint( fn=tradeoffs.tradeoff ))
constraints[0].pxds.append( pxds[0] )

# define instruments
instrumentTypes=[]
instrumentTypes.append( InstrumentType(title='X-Strain',abv='exx',unit='ns') )
instrumentTypes.append( InstrumentType(title='Y-Strain',abv='eyy',unit='ns') )
instrumentTypes.append( InstrumentType(title='Z-Strain',abv='ezz',unit='ns') )
instrumentTypes.append( InstrumentType(title='XY-Shear',abv='exy',unit='ns') )
instrumentTypes.append( InstrumentType(title='X-Tilt',abv='gUxZ',unit='1') )
instrumentTypes.append( InstrumentType(title='Y-Tilt',abv='gUyZ',unit='1') )
instrumentTypes.append( InstrumentType(title='Fluid Pressure',abv='pf',unit='kPa') )

geom_avn2 = np.array([ +239.8,  -75.3, +515.0 ])
geom_avn3 = np.array([ +206.8,  -60.5, +495.0 ])
geom_11a  = np.array([ +374.6, -199.1,   -3.5 ])
geom_27   = np.array([ -375.9,   -5.4,   -3.5 ])
geom_29   = np.array([ -185.0,  +28.7,   -3.5 ])
geom_60   = np.array([ -245.0, -111.7,   -3.5 ])
geom_9A   = np.array([   +0.0,   -0.0,   -3.5 ])

instruments=[]
instruments.append( Instrument(title='avn2 exx1',geom=geom_avn2) )
instruments.append( Instrument(title='avn2 eyy1',geom=geom_avn2) )
instruments.append( Instrument(title='avn2 ezz1',geom=geom_avn2) )
instruments.append( Instrument(title='avn2 exy1',geom=geom_avn2) )

instruments.append( Instrument(title='avn3 gUxZ',geom=geom_avn3) )
instruments.append( Instrument(title='avn3 gUyZ',geom=geom_avn3) )

instruments.append( Instrument(title='11a pf',geom=geom_11a) )
instruments.append( Instrument(title='27 pf',geom=geom_27) )
instruments.append( Instrument(title='29 pf',geom=geom_29) )
instruments.append( Instrument(title='60 pf',geom=geom_60) )
instruments.append( Instrument(title='9A pf',geom=geom_9A) )

instruments[0].instType  = instrumentTypes[0]
instruments[1].instType  = instrumentTypes[1]
instruments[2].instType  = instrumentTypes[2]
instruments[3].instType  = instrumentTypes[3]
instruments[4].instType  = instrumentTypes[4]
instruments[5].instType  = instrumentTypes[5]
instruments[6].instType  = instrumentTypes[6]
instruments[7].instType  = instrumentTypes[6]
instruments[8].instType  = instrumentTypes[6]
instruments[9].instType  = instrumentTypes[6]
instruments[10].instType = instrumentTypes[6]

# define forward models
fmods=[]
fmods.append(ForwardModel(fmod=forwardModels.buildInput))

t=[]
exx=[]
eyy=[]
ezz=[]
exy=[]
pf1=[]
pf2=[]
pf3=[]
pf4=[]
pf5=[]
file=open('2017284-2017290_9a_injection.txt','rb')
for line in file:
  t.append(   line[:-1].split(',')[0] )
  eyy.append( line[:-1].split(',')[1] )
  exx.append( line[:-1].split(',')[2] )
  ezz.append( line[:-1].split(',')[4] )
  exy.append( line[:-1].split(',')[3] )

  pf1.append( line[:-1].split(',')[5] )
  pf2.append( line[:-1].split(',')[6] )
  pf3.append( line[:-1].split(',')[7] )
  pf4.append( line[:-1].split(',')[8] )
  pf5.append( line[:-1].split(',')[9] )

t   = np.array(t,dtype='float')
exx = np.array(exx,dtype='float')
eyy = np.array(eyy,dtype='float')
ezz = np.array(ezz,dtype='float')
exy = np.array(exy,dtype='float')
pf1 = np.array(pf1,dtype='float')
pf2 = np.array(pf2,dtype='float')
pf3 = np.array(pf3,dtype='float')
pf4 = np.array(pf4,dtype='float')
pf5 = np.array(pf5,dtype='float')

t-=t[0]
exx-=exx[0]
eyy-=eyy[0]
ezz-=ezz[0]
exy-=exy[0]
pf1-=pf1[0]
pf2-=pf2[0]
pf3-=pf3[0]
pf4-=pf4[0]
pf5-=pf5[0]

t = t/86400.0

ntr  = 3500
tr   = np.linspace(np.min(t),np.max(t),ntr).reshape(ntr,1)
exxr = np.interp(tr,t,exx).reshape(ntr,1)
eyyr = np.interp(tr,t,eyy).reshape(ntr,1)
ezzr = np.interp(tr,t,ezz).reshape(ntr,1)
exyr = np.interp(tr,t,exy).reshape(ntr,1)
pf1r = np.interp(tr,t,pf1).reshape(ntr,1)
pf2r = np.interp(tr,t,pf2).reshape(ntr,1)
pf3r = np.interp(tr,t,pf3).reshape(ntr,1)
pf4r = np.interp(tr,t,pf4).reshape(ntr,1)
pf5r = np.interp(tr,t,pf5).reshape(ntr,1)

tr_exxr = np.hstack((tr,exxr))
tr_eyyr = np.hstack((tr,eyyr))
tr_ezzr = np.hstack((tr,ezzr))
tr_exyr = np.hstack((tr,exyr))
tr_pf1r = np.hstack((tr,pf1r))
tr_pf2r = np.hstack((tr,pf2r))
tr_pf3r = np.hstack((tr,pf3r))
tr_pf4r = np.hstack((tr,pf4r))
tr_pf5r = np.hstack((tr,pf5r))

indVars = np.linspace(0,25*86400,3000)

measurements = []
measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_exxr, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))
measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_eyyr, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))
measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_ezzr, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))
measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_exyr, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))

measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_exyr, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))
measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_exyr, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))

measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_pf1r, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))
measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_pf2r, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))
measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_pf3r, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))
measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_pf4r, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))
measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=tr, data=tr_pf5r, sigsq=1.0, weight=1.0, detrend=detrend.detrend ))

measurements[0].instruments.append(  instruments[0]  )
measurements[1].instruments.append(  instruments[1]  )
measurements[2].instruments.append(  instruments[2]  )
measurements[3].instruments.append(  instruments[3]  )
measurements[4].instruments.append(  instruments[4]  )
measurements[5].instruments.append(  instruments[5]  )
measurements[6].instruments.append(  instruments[6]  )
measurements[7].instruments.append(  instruments[7]  )
measurements[8].instruments.append(  instruments[8]  )
measurements[9].instruments.append(  instruments[9]  )
measurements[10].instruments.append( instruments[10] )

signalTypes = []
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[0]) )
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[1]) )
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[2]) )
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[3]) )
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[4]) )
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[5]) )
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[6]) )
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[7]) )
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[8]) )
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[9]) )
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[10]) )

# define objectives
objectives = []
objectives.append( Objective( post=postProcessors.exx ) )
objectives.append( Objective( post=postProcessors.eyy ) )
objectives.append( Objective( post=postProcessors.exy ) )
objectives.append( Objective( post=postProcessors.exy ) )
objectives.append( Objective( post=postProcessors.exy ) )
objectives.append( Objective( post=postProcessors.exy ) )
objectives.append( Objective( post=postProcessors.exy ) )
objectives.append( Objective( post=postProcessors.exy ) )
objectives.append( Objective( post=postProcessors.exy ) )
objectives.append( Objective( post=postProcessors.exy ) )
objectives.append( Objective( post=postProcessors.exy ) )

objectives[0].measurements.append(  measurements[0]  )
objectives[1].measurements.append(  measurements[1]  )
objectives[2].measurements.append(  measurements[2]  )
objectives[3].measurements.append(  measurements[3]  )
objectives[4].measurements.append(  measurements[4]  )
objectives[5].measurements.append(  measurements[5]  )
objectives[6].measurements.append(  measurements[6]  )
objectives[7].measurements.append(  measurements[7]  )
objectives[8].measurements.append(  measurements[8]  )
objectives[9].measurements.append(  measurements[9]  )
objectives[10].measurements.append( measurements[10] )

opts = []
opts.append(OptLHC(aws_id=aws_id,aws_key=aws_key,bucket=bucket))
opts.append(OptNSGAII(aws_id=aws_id,aws_key=aws_key,bucket=bucket))
opts.append(OptPareto(aws_id=aws_id,aws_key=aws_key,bucket=bucket))
session.add_all(opts)

opts[0].objectives+=objectives
opts[1].objectives+=objectives
opts[2].objectives+=objectives
opts[0].pxds+=pxds
opts[1].pxds+=pxds
opts[2].pxds+=pxds

parameters = opts[0].random_parameterization()

opts[0].parameters=parameters
opts[1].parameters=parameters
opts[2].parameters=parameters

session.commit()

opts[0].generate_samples(50000,{'n':50000})
opts[1].startup()
opts[2].startup()

session.commit()

times = np.zeros([0,7],dtype='float')
pickle.dump(times,open('times.pkl','wb'))
