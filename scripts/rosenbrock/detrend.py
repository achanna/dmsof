import sys
sys.path.append('/home/achanna/Dropbox/poroelast7/imports/misc')
from header import *

def detrend(prediction):
  iv  = np.copy(prediction.measurement.indVars_prescribed)
  si  = np.copy(prediction.data)
  return iv,si
