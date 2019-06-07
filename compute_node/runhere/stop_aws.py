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

s3  = S3Connection( aws_access_key_id=aws_id, aws_secret_access_key=aws_key )

b = s3.get_bucket(bucket)
k = b.get_key('stop')
k.get_contents_to_filename('stop_aws.pkl')
stop = pickle.load(open('stop_aws.pkl','rb'))
if stop==1:
  print 'breaking loop'
  exit(1)
else:    exit(0)
