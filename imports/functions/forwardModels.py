import sys
sys.path.append('../misc')
from header import *
from connect_info import *

def assemble_model(sample):
  model = []
  for estimate in sample.estimates: model.append(estimate.value)
  for simulation in sample.simulations:
    for prediction in simulation.predictions:
      model.append( prediction.id )
      for coord in prediction.objective.instrument.geom:
        model.append( coord )
      model.append( prediction.objective.instrument.instType.abv )
      model.append( 0 )
      model[-1] = prediction.objective.instrument.indVars
  return model

def pushInput(simulation,aws_id,aws_key,bucket):
  while True:
    try:
      s3  = S3Connection( aws_access_key_id=aws_id, aws_secret_access_key=aws_key )
      sqs = boto.sqs.connect_to_region("us-west-2", aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
      b = s3.get_bucket(bucket)
      q = sqs.get_queue('%s_input' % bucket)
      k = Key(b)
      m = Message(q)
      k.key = 'input_%i' % simulation.id
      k.set_contents_from_filename('input-files.tgz')
      m.set_body('%i' % simulation.id)
      q.write(m)
      simulation.inputFilePushed=True
    except:
      print 'Connection error, pausing for 10 seconds before re-try...'
      time.sleep(10)
    else: break

def buildPush(objective,buildInput):
  opt = simulation.sample.optimization
  aws_id  = opt.aws_id
  aws_key = opt.aws_key
  bucket  = opt.bucket
  model = assemble_model(simulation)
  buildInput(model)
  pushInput(simulation,aws_id,aws_key,bucket)
