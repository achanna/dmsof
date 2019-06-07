import pickle
import math
import sys
import time
import scipy
import scipy.io
import scipy.interpolate
import numpy as np
import string
import datetime

t=[]
t.append(datetime.datetime.utcnow())
pickle.dump({'times':t},open('output.pkl','wb'))

model=pickle.load(open('model.pkl','rb'))['model']

input_file = open('input.geo','a')
for id_signalType, signal in model['signals'].iteritems():
  for id_instrument, value in signal['instruments'].iteritems():
    geom = value['geom']
    abv  = value['abv']
    if abv=='gUxZ' or abv=='gUyZ':
      input_file.write('      POINT_%07i "%f %f %f"\n'  % (int(id_signalType),geom[0],geom[1],geom[2]))
      input_file.write('      POINT_%07ia "%f %f %f"\n' % (int(id_signalType),geom[0],geom[1],geom[2]+49))
      input_file.write('      POINT_%07ib "%f %f %f"\n' % (int(id_signalType),geom[0],geom[1],geom[2]-49))
    else:
      input_file.write('      POINT_%07i "%f %f %f"\n'  % (int(id_signalType),geom[0],geom[1],geom[2]))

input_file.write('    }\n')
input_file.write('  }\n')
input_file.write('  BOUNDARY_PENALTY 1e10\n')
input_file.write('}\n')
input_file.close()

