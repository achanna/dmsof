import sys
sys.path.append('/home/ubuntu/visit2_12_2.linux-x86_64/2.12.2/linux-x86_64/lib/site-packages/')
import visit
import numpy as np
import pickle

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

visit.LaunchNowin()

visit.OpenDatabase('solution.visit')
visit.AddPlot("Pseudocolor", "pressure")
visit.DrawPlots()

'''plt.figure()
for i in range(20):
  xyz = (0,y[i],+28)
  nts = visit.TimeSliderGetNStates()
  p1 = np.zeros(nts,dtype='float')
  for ts in range(nts):
    visit.TimeSliderSetState(ts)
    visit.Pick(xyz)
    pick=visit.GetPickOutput()
    for line in range(8):
      p1[ts] += np.float(pick.splitlines()[7+line].split()[2])
    p1[ts] /= 8.0
    visit.ClearPickPoints()
  plt.plot(t,p1*1e-3,c=cmap.to_rgba(y[i]))'''
