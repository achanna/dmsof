import sys
sys.path.append('/home/ubuntu/poroelast9/imports/misc')
from header import *

import detrend
import tradeoffs
import likelihoods
import forwardModels
import postProcessors
from connect_info import *

stop=0
pickle.dump(stop,open('stop_aws.pkl','wb'))

s3  = S3Connection( aws_access_key_id=aws_id, aws_secret_access_key=aws_key )
b = s3.get_bucket(bucket)

k = Key(b)
k.key = 'stop'
k.set_contents_from_filename('stop_aws.pkl')

s3.close()

