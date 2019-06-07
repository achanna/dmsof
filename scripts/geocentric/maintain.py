import sys
sys.path.append('/home/ubuntu/poroelast9/imports/misc')
from header import *

import detrend
import tradeoffs
import likelihoods
import forwardModels
import postProcessors
from connect_info import *

sqs = boto.sqs.connect_to_region("us-west-2", aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
qi  = sqs.get_queue('%s_input' % bucket)
qs  = sqs.get_queue('%s_start' % bucket)
qo  = sqs.get_queue('%s_output' % bucket)

print '%i simulations standing by with input files built' % qi.count()
print '%i simulations in the started pool' % qs.count()
print '%i simulations completed, waiting for post-processing' % qo.count()

t0=time.time()
engine  = sqlalchemy.create_engine('mysql+mysqldb://%s:%s@localhost/%s'%(db_user,db_pswd,db_title), echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

opts = session.query(Optimization).all()
objs = session.query(Objective).all()

opts[0].retrieve_results()
opts[0].integrate_signals()
session.commit()

opts[0].generate_samples(50,{'n':50})
session.commit()
exit()

nn=25
nm=200

t0=time.time()
if qi.count()<2000:

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,6])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,6])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([1,7])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([1,7])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,2])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,2])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,7])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,7])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([1,6])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([1,6])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([1,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([1,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([6,7])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([6,7])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([6,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([6,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[1].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

  opts[0].retrieve_results()
  opts[0].integrate_signals()
  session.commit()
  opts[2].generate_samples(nn,{'N':nm,'objs':np.array(objs)[np.array([0,1,2,6,7,8])],'tournament_size':2})
  session.commit()

#time.sleep(1800)
opts[0].retrieve_results()
opts[0].integrate_signals()
session.commit()
print time.time()-t0
