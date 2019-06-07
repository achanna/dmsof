import sys
sys.path.append('/home/achanna/Dropbox/poroelast8/imports/misc')
from header import *
from connect_info import *

def buildInput(model):

  pickle.dump({'model':model},open('model.pkl','wb'))
  os.system('tar cvzf input-files.tgz model.pkl > /dev/null 2>&1')

def rosenbrock():
  t=[]
  t.append(datetime.datetime.utcnow())
  model=pickle.load(open('model.pkl','rb'))['model']
  x=np.zeros([2],dtype='float')
  for id_estimate,estimate in model['estimates'].iteritems():
    if estimate['abv']=='x01': x[0] = estimate['value']
    if estimate['abv']=='x02': x[1] = estimate['value']
  output = {}
  for id_signalType, signal in model['signals'].iteritems():
    for id_instrument,instrument in signal['instruments'].iteritems():
      abv = instrument['abv']
      a = 1
      b = 100
      f = a*(x[0]-1)**2+b*(x[1]-x[0]**2)**2
      output[id_signalType] = np.array([f])
  t.append(datetime.datetime.utcnow())
  pickle.dump({'output':output,'times':t},open('output.pkl','wb'))
