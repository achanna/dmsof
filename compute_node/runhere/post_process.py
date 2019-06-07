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

sys.path.append('/home/ubuntu/visit2_12_2.linux-x86_64/2.12.2/linux-x86_64/lib/site-packages/')
import visit

visit.LaunchNowin()
visit.OpenDatabase('solution.visit')
visit.AddPlot("Pseudocolor", "pressure")
visit.DrawPlots()

times=pickle.load(open('output.pkl','rb'))['times']

model=pickle.load(open('model.pkl','rb'))['model']

datacols = {}
datacols['pf'] = 4
datacols['ux'] = 1
datacols['uy'] = 2
datacols['uz'] = 3
datacols['exx'] = 11
datacols['eyy'] = 12
datacols['ezz'] = 13
datacols['exy'] = 16

i=0
output = {}
print output
for id_signalType, signal in model['signals'].iteritems():
  indVars = signal['indVars']
  for id_instrument,instrument in signal['instruments'].iteritems():

    abv = instrument['abv']
    geom = instrument['geom']
    print abv, geom, i, len(model['signals'].keys())
    t = np.loadtxt('./solution-point-%07i.txt' % id_signalType)[:,0]
    if 'ear'==abv:
      exx = np.loadtxt('./solution-point-%07i.txt' % id_signalType)[:,datacols['exx']]
      eyy = np.loadtxt('./solution-point-%07i.txt' % id_signalType)[:,datacols['eyy']]
      d   = exx+eyy
    elif 'gUxZ'==abv:
      ux0 = np.loadtxt('./solution-point-%07ia.txt' % id_signalType)[:,datacols['ux']]
      ux1 = np.loadtxt('./solution-point-%07ib.txt' % id_signalType)[:,datacols['ux']]
      d   = (ux1-ux0)/80.0
    elif 'gUyZ'==abv:
      ux0 = np.loadtxt('./solution-point-%07ia.txt' % id_signalType)[:,datacols['uy']]
      ux1 = np.loadtxt('./solution-point-%07ib.txt' % id_signalType)[:,datacols['uy']]
      d   = (ux1-ux0)/80.0
    #elif abv=='pf':
    #  xyz = (geom[0],geom[1],geom[2])
    #  nts = visit.TimeSliderGetNStates()
    #  p1 = np.zeros(nts,dtype='float')
    #  for ts in range(nts):
    #    visit.TimeSliderSetState(ts)
    #    visit.Pick(xyz)
    #    pick=visit.GetPickOutput()
    #    for line in range(8):
    #      p1[ts] += np.float(pick.splitlines()[7+line].split()[2])
    #    p1[ts] /= 8.0
    #    visit.ClearPickPoints()
    #  d=p1
    else:
      d   = np.loadtxt('./solution-point-%07i.txt'  % id_signalType)[:,datacols[abv]]
    output[id_signalType] = np.interp(indVars,t,d)
    i+=1

times.append(datetime.datetime.utcnow())

pickle.dump({'output':output,'times':times},open('output.pkl','wb'))
