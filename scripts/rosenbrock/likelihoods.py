import sys
sys.path.append('/home/achanna/Dropbox/poroelast7/imports/misc')
from header import *

def likelihood(prediction):
  w = 2.65
  a = 26.0
  e = np.log10(prediction.objective.measurement.sigsq)*0.9
  x = np.log10(prediction.fetch_misfit())
  t = (x-e)/w
  pdf = 1.0/(2.0*math.pi)**0.5 * np.exp(-t**2.0/2.0)
  cdf = (1.0+scipy.special.erf((t*a)/2.0**0.5))/2.0
  return 2.0 / w * pdf * cdf

def interp_model_to_grid(sample):
  rho = []
  for estimate in sample.estimates:
    rho.append( estimate.value )

  ell1 = matplotlib.patches.Ellipse( (+40,-30), +20, +40, +60 )
  ell2 = matplotlib.patches.Ellipse( (-30,-20), +18, +60, -15 )

  x = np.linspace(-100,100,200)
  y = np.linspace(-100,0,100)
  X,Y = np.meshgrid(x,y)
  D = np.zeros(X.shape)
  for i in range(X.shape[0]):
    for j in range(X.shape[0]):
      ix = X[i,j]
      iy = Y[i,j]
      if   ell1.contains_point((ix,iy)): D[i,j] = rho[1]
      elif ell2.contains_point((ix,iy)): D[i,j] = rho[2]
      else: D[i,j] = rho[0]

  return D
