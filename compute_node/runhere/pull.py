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
b  = s3.get_bucket(bucket)

while True:
  sys.stdout.write('Checking queue for new input files (visibility timeout 5 minutes)\n')
  sys.stdout.flush()
  m = qi.read(300)
  if m==None:
    sys.stdout.write('...no new input files available on queue, breaking loop\n')
    sys.stdout.flush()
    exit(1)
  else:
    sys.stdout.write('...queue message found, reading\n')
    sys.stdout.flush()
    id_simulation = m.get_body()
    sys.stdout.write('...message read, searching S3 bucket for input files (id_simulation=%i)\n' % int(id_simulation) )
    sys.stdout.flush()
    file=open('id_simulation','w')
    file.write(id_simulation)
    file.close()

    try:
      sys.stdout.write('...downloading input files\n')
      sys.stdout.flush()
      k=b.get_key('input_%i' % int(id_simulation) )
      k.get_contents_to_filename('input-files.tgz')

    except:
      sys.stdout.write('...error downloading input files, break\n')
      sys.stdout.flush()
      break

    else:
      sys.stdout.write('...input files downloaded successfully\n' )
      sys.stdout.flush()

      sys.stdout.write('...deleting input queue message\n' )
      sys.stdout.flush()
      qi.delete_message(m)

      sys.stdout.write('...pushing start queue message\n')
      sys.stdout.flush()
      m=Message()
      m.set_body(id_simulation)
      qs.write(m)

      break
