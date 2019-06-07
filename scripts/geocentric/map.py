import numpy as np
import matplotlib as mpl
from matplotlib import patches
mpl.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

plt.figure()

geom_avn2 = np.array([ +239.8,  -75.3, +515.0 ])
geom_27   = np.array([ -375.9,   -5.4,   -3.5 ])
geom_29   = np.array([ -185.0,  +28.7,   -3.5 ])
geom_60   = np.array([ -245.0, -111.7,   -3.5 ])
geom_9A   = np.array([   +0.0,   -0.0,   -3.5 ])

plt.scatter( geom_avn2[0],	geom_avn2[1], s=50, c='r', zorder=1 )
plt.scatter( geom_27[0],	geom_27[1],   s=50, c='r', zorder=1 )
plt.scatter( geom_29[0],	geom_29[1],   s=50, c='r', zorder=1 )
plt.scatter( geom_60[0],	geom_60[1],   s=50, c='r', zorder=1 )
plt.scatter( geom_9A[0],	geom_9A[1],   s=50, c='r', zorder=1 )

plt.text( geom_avn2[0],	geom_avn2[1], 'AVN2', fontsize=24, zorder=2 )
plt.text( geom_27[0],	geom_27[1],   '27',   fontsize=24, zorder=2 )
plt.text( geom_29[0],	geom_29[1],   '29',   fontsize=24, zorder=2 )
plt.text( geom_60[0],	geom_60[1],   '60',   fontsize=24, zorder=2 )
plt.text( geom_9A[0],	geom_9A[1],   '9A',   fontsize=24, zorder=2 )

plt.plot( [geom_avn2[0],geom_9A[0]], [geom_avn2[1],geom_9A[1]], '--', lw=2, zorder=0 )

plt.fill( [-50,-50,+200,+200,-50],[-220,-215,-215,-220,-220], facecolor=[0.6,0.6,0.6] )
plt.plot( [-0,-0],[-220,-215], c='k' )
plt.plot( [+50,+50],[-220,-215], c='k' )
plt.plot( [+100,+100],[-220,-215], c='k' )
plt.plot( [+150,+150],[-220,-215], c='k' )

plt.text( +75, -214, '250 meters', fontsize=22, horizontalalignment='center', verticalalignment='bottom' )

plt.xlim([-400,+300])
plt.ylim([-400,+300])
plt.axis('off')
plt.savefig('map.eps',format='eps',bbox_inches='tight')
plt.close()
