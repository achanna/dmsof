import sys
sys.path.append('/home/achanna/Dropbox/poroelast7/imports/misc')
from header import *

'''def detrend(prediction):
  iv  = np.copy(prediction.measurement.indVars_prescribed)
  si  = np.copy(prediction.data)
  iv /= 86400.0
  si *= 1e9
#  i1  = np.where(iv>=-50)[0][0]
#  i2  = np.where(iv>=0)[0][0]
#  f   = np.polyfit( iv[i1:i2], si[i1:i2], 1 )
#  si -= (f[0]*iv+f[1])
  si -= si[0]
  iv += 7
  si = np.append( 0,si )
  iv = np.append( 0,iv )
  return iv,si'''

def detrend(prediction):
  iv  = np.copy(prediction.measurement.indVars_prescribed)
  si  = np.copy(prediction.data)
  iv /= 86400.0
  iv += 6.8
  abv = prediction.measurement.instruments[0].instType.abv
  iv  = np.concatenate([[0],iv])
  si  = np.concatenate([[0],si])
  if   abv=='exx':  si *= +1e+9
  elif abv=='eyy':  si *= +1e+9
  elif abv=='ezz':  si *= +1e+9
  elif abv=='exy':  si *= +1e+9

#  elif abv=='gUxZ': si *= +1e+9
#  elif abv=='gUyZ': si *= +1e+9

  else:             si *= +1e-3
  return iv,si
