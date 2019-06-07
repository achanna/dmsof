import sys
sys.path.append('/home/achanna/poroelast9/imports/misc')
from header import *

import detrend
import tradeoffs
import likelihoods
import forwardModels
import postProcessors
from connect_info import *

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

# define physical properties
properties=[]
properties.append( Property( title='x01', abv='x01', unit='1'  ))
properties.append( Property( title='x02', abv='x02', unit='1' ))

# define geometry and model domains
domains=[]
domains.append( Domain( title='Domain', geom=np.array([[0,2000],[0,2000],[-250,+500]]) ))

# define prior probability distributions, define pxds

priorModel0 = Uniform( -1.00, +1.00, 0.05 )
priorModel1 = Uniform( -1.00, +1.00, 0.05 )

pxds=[]
pxds.append( Prop_X_Domain( property=properties[0], domain=domains[0], priorModel=priorModel0 ))
pxds.append( Prop_X_Domain( property=properties[1], domain=domains[0], priorModel=priorModel1 ))

constraints=[]

# define instruments
instrumentTypes=[]
instrumentTypes.append( InstrumentType(title='f1',abv='f1',unit='1') )

geom = np.array([0,0,0])

instruments=[]
instruments.append( Instrument(title='f1',geom=geom) )
instruments[0].instType = instrumentTypes[0]

# define forward models
fmods=[]
fmods.append(ForwardModel(fmod=forwardModels.buildInput))

indVars = np.array([0])

measurements = []
measurements.append(Measurement( indVars_prescribed=indVars, indVars_actual=indVars.copy(), data=indVars.copy(), sigsq=1.0, weight=1.0, detrend=detrend.detrend ))

measurements[0].instruments.append( instruments[0] )

signalTypes = []
signalTypes.append( SignalType(forwardModel=fmods[0],measurement=measurements[0]) )

# define objectives
objectives = []
objectives.append( Objective( post=postProcessors.f1 ) )

objectives[0].measurements.append( measurements[0] )

opts = []
opts.append(OptMC(aws_id=aws_id,aws_key=aws_key,bucket=bucket))
session.add_all(opts)

opts[0].objectives+=objectives
opts[0].pxds+=pxds
opts[0].parameters=opts[0].random_parameterization()

session.commit()

times = np.zeros([0,7],dtype='float')
pickle.dump(times,open('times.pkl','wb'))
