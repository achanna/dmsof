import os
import sys
import time
import scipy
import scipy.io
import pickle
import numpy
from connect_info import *

import boto
import boto.s3
import boto.sqs
from boto.sqs.message import Message
from boto.s3.connection import S3Connection
from boto.s3.key import Key

sqs = boto.sqs.connect_to_region("us-west-2", aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
s3  = S3Connection( aws_access_key_id=aws_id, aws_secret_access_key=aws_key )

qi = sqs.get_queue('%s_input' % bucket)
qs = sqs.get_queue('%s_start' % bucket)
qo = sqs.get_queue('%s_output' % bucket)
b = s3.get_bucket(bucket)

while True:

  try:
    sys.stdout.write('...beginning push phase\n')
    sys.stdout.flush()
    id_simulation = open('id_simulation','r').read()

    sys.stdout.write('...pushing output file\n')
    sys.stdout.flush()
    k = Key(b)
    k.key = 'output_%i' % int(id_simulation)
    k.set_contents_from_filename('output.pkl')

    sys.stdout.write('...pushing output message\n')
    sys.stdout.flush()
    m = Message(qo)
    m.set_body(id_simulation)
    qo.write(m)

  except:
    sys.stdout.write('Error, retrying postprocess of id_simulation=%i\n' % int(id_simulation) )
    sys.stdout.flush()
    time.sleep(15)

  else:
    sys.stdout.write('...output file and message pushed successfully\n')
    sys.stdout.flush()
    break
