import sys
sys.path.append('/home/achanna/Dropbox/poroelast8/imports/misc')
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

engine  = sqlalchemy.create_engine('mysql+mysqldb://%s:%s@localhost/%s'%(db_user,db_pswd,db_title), echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

opts = session.query(Optimization).all()

print len(opts[0].get_complete_samples())

for opt in opts:
  print len(opt.samples)

