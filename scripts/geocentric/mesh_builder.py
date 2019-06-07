import sys
import math
import numpy as np
sys.path.append('/opt/Trelis-16.4/bin/')
import cubit

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

import shapely
import shapely.geometry
import scipy
import scipy.linalg
import scipy.optimize
import functools
import pickle

cubit.init(['test','-nojournal'])
cubit.cmd('reset')
cubit.cmd('create brick x 20000 y 20000 z 645')
cubit.cmd('move volume all x 0 y 0 z +222.5')

cubit.cmd('webcut body all with general plane xy move x 0 y 0 z 0')
cubit.cmd('webcut body all with general plane xy move x 0 y 0 z 27')
cubit.cmd('webcut body all with general plane xy move x 0 y 0 z -5')
cubit.cmd('webcut body all with general plane yz move x -1000 y 0 z 0')
cubit.cmd('webcut body all with general plane yz move x +1000 y 0 z 0')
cubit.cmd('webcut body all with general plane xz move x 0 y -1000 z 0')
cubit.cmd('webcut body all with general plane xz move x 0 y +1000 z 0')

xmin=cubit.get_total_bounding_box('volume',cubit.get_entities('volume'))[0]
xmax=cubit.get_total_bounding_box('volume',cubit.get_entities('volume'))[1]
ymin=cubit.get_total_bounding_box('volume',cubit.get_entities('volume'))[3]
ymax=cubit.get_total_bounding_box('volume',cubit.get_entities('volume'))[4]
zmin=cubit.get_total_bounding_box('volume',cubit.get_entities('volume'))[6]
zmax=cubit.get_total_bounding_box('volume',cubit.get_entities('volume'))[7]

cubit.cmd('webcut volume all with cylinder radius 20.0 axis z center 0,0,0' )
cubit.cmd('webcut volume all with cylinder radius  2.0 axis z center 0,0,0' )
cubit.cmd('webcut volume all with cylinder radius  1.8 axis z center 0,0,0' )

cubit.cmd('webcut volume all with cylinder radius  2.0 axis z center %f,%f,%f' % (+239.8,  -75.3,  +515.0) )
cubit.cmd('webcut volume all with cylinder radius  2.0 axis z center %f,%f,%f' % (-185.0,  +28.7,    -3.0) )

for icurve in cubit.get_entities('curve'):
  l  = cubit.get_curve_length(icurve)
  r1 = 2*math.pi*1.8
  r2 = 2*math.pi*2.0
  r3 = 2*math.pi*20.0
  if cubit.get_relatives('curve',icurve,'volume')>36:
    if np.abs(l-r1)<0.01 or np.abs(l-r2)<0.01:
      cubit.cmd('curve %i interval 6' % icurve)
    if np.abs(l-r3)<0.01:
      cubit.cmd('curve %i interval 12' % icurve)

for ivol in cubit.get_entities('volume'):
  for icurve in cubit.get_relatives('volume',ivol,'curve'):
    v = [cubit.vertex(ivertex) for ivertex in cubit.get_relatives('curve',icurve,'vertex')]
    if len(v)==2:
      x0,y0,z0 = v[0].coordinates()
      x1,y1,z1 = v[1].coordinates()
      if np.abs(x0-x1)<0.01 and np.abs(y0-y1)<0.01:
        z = 0.5*(z0+z1)
        if   z<-5:
          intv = 3
          bias = 0.7
          if z0>z1: cubit.cmd('curve %i interval %i scheme bias {1/%f}' % (icurve,intv,bias) )
          else:     cubit.cmd('curve %i interval %i scheme bias %f'     % (icurve,intv,bias) )
        elif z<+0:  cubit.cmd('curve %i interval 1' % icurve)
        elif z<+27:
          intv = 2
          bias = 1.0
          if z0>z1: cubit.cmd('curve %i interval %i scheme bias %f'     % (icurve,intv,bias) )
          else:     cubit.cmd('curve %i interval %i scheme bias {1/%f}' % (icurve,intv,bias) )
        else:
          bias = 0.82
          intv = 7
          if z0>z1: cubit.cmd('curve %i interval %i scheme bias %f'     % (icurve,intv,bias) )
          else:     cubit.cmd('curve %i interval %i scheme bias {1/%f}' % (icurve,intv,bias) )

for ivol in cubit.get_entities('volume'):
  for icurve in cubit.get_relatives('volume',ivol,'curve'):
    v = [cubit.vertex(ivertex) for ivertex in cubit.get_relatives('curve',icurve,'vertex')]
    if len(v)==2:
      x0,y0,z0 = v[0].coordinates()
      x1,y1,z1 = v[1].coordinates()
      if ivol in cubit.get_entities('volume'):
        if np.abs(y0-y1)<0.1 and np.abs(z0-z1)<0.1 and np.abs(0.5*(x0+x1)-0)>1000:
          bias = 0.70
          intv = 6
          if 0.5*(x0+x1)<0:
            if x0<x1: cubit.cmd('curve %i interval %i scheme bias %f'     % (icurve,intv,bias) )
            else:     cubit.cmd('curve %i interval %i scheme bias {1/%f}' % (icurve,intv,bias) )
          else:
            if x0<x1: cubit.cmd('curve %i interval %i scheme bias {1/%f}' % (icurve,intv,bias) )
            else:     cubit.cmd('curve %i interval %i scheme bias %f'     % (icurve,intv,bias) )
        if np.abs(x0-x1)<0.1 and np.abs(z0-z1)<0.1 and np.abs(0.5*(y0+y1)-0)>1000:
          bias = 0.70
          intv = 6
          if 0.5*(y0+y1)<0:
            if y0<y1: cubit.cmd('curve %i interval %i scheme bias %f'     % (icurve,intv,bias) )
            else:     cubit.cmd('curve %i interval %i scheme bias {1/%f}' % (icurve,intv,bias) )
          else:
            if y0<y1: cubit.cmd('curve %i interval %i scheme bias {1/%f}' % (icurve,intv,bias) )
            else:     cubit.cmd('curve %i interval %i scheme bias %f'     % (icurve,intv,bias) )

for ivol in cubit.get_entities('volume'):
  if ivol in range(1,29) or ivol in range(33,37):
    for icurve in cubit.get_relatives('volume',ivol,'curve'):
      v = [cubit.vertex(ivertex) for ivertex in cubit.get_relatives('curve',icurve,'vertex')]
      if len(v)==2:
        x0,y0,z0 = v[0].coordinates()
        x1,y1,z1 = v[1].coordinates()
      if np.abs(y0-y1)<0.01 and np.abs(z0-z1)<0.01 and np.abs(0.5*(x0+x1)-0)<1:
        intv = 14
        bias = 0.97
        cubit.cmd('curve %i interval %i scheme dualbias %f' % (icurve,intv,bias) )
      if np.abs(x0-x1)<0.01 and np.abs(z0-z1)<0.01 and np.abs(0.5*(y0+y1)-0)<1:
        intv = 14
        bias = 0.97
        cubit.cmd('curve %i interval %i scheme dualbias %f' % (icurve,intv,bias) )

cubit.cmd('imprint body all')
cubit.cmd('merge body all')
cubit.cmd('mesh volume all')

for isurf in cubit.get_entities('surface'):
  x0,y0,z0 = cubit.get_surface_centroid(isurf)
  c0       = cubit.get_surface_normal(isurf)
  if c0[1]==1 or c0[1]==-1:
    if np.abs(y0-ymin)<0.1:
      cubit.cmd('sideset 1 add surface %i' % isurf)	# N
    if np.abs(y0-ymax)<0.1:
      cubit.cmd('sideset 2 add surface %i' % isurf)	# S
  if c0[0]==1 or c0[0]==-1:
    if np.abs(x0-xmin)<0.1:
      cubit.cmd('sideset 3 add surface %i' % isurf)	# E
    if np.abs(x0-xmax)<0.1:
      cubit.cmd('sideset 4 add surface %i' % isurf)	# W
  if c0[2]==1 or c0[2]==-1:
    if np.abs(z0-zmin)<0.1:
      cubit.cmd('sideset 5 add surface %i' % isurf)	# lower
    if np.abs(z0-zmax)<0.1:
      isWell=False
      ovol = cubit.get_owning_volume('surface',isurf)
      if np.sum((np.array([0,0])-np.array(cubit.get_center_point('volume',ovol)[0:2]))**2)**0.5<0.1:
        if np.abs(cubit.get_surface_area(isurf)-(math.pi*1.8**2))<0.01:
          print ovol
          isWell=True
      if isWell: cubit.cmd('sideset 7 add surface %i' % (isurf))	# injection
      else:      cubit.cmd('sideset 6 add surface %i' % isurf)		# upper

hex_ids   = np.zeros([0,3],dtype='int')
hex_xyzs  = np.zeros([0,3],dtype='float')
hex_types = np.zeros([0,1],dtype='float')
iblock=0
for ivol in range(1,cubit.get_volume_count()+1):
  for ihex in cubit.get_volume_hexes(ivol):
    iblock+=1
    cubit.cmd('block %i add hex %i' % (iblock,ihex) )
    x,y,z = cubit.get_center_point("hex",ihex)
    hex_ids   = np.concatenate( [hex_ids,  np.array([ivol,iblock,ihex]).reshape(1,3)], axis=0 )
    hex_xyzs  = np.concatenate( [hex_xyzs, np.array([x,y,z]).reshape(1,3)], axis=0 )
    isWell = False
    isCase = False

    if ivol in range(37+0,37+4):  pass
    if ivol in range(37+4,37+8):  isCase = True
    if ivol in range(37+8,37+12): isWell = True

    if   isWell:          hex_types = np.concatenate( [hex_types, np.array([0]).reshape(1,1)], axis=0 )
    elif isCase:          hex_types = np.concatenate( [hex_types, np.array([1]).reshape(1,1)], axis=0 )
    elif -5<=z and z<=0:  hex_types = np.concatenate( [hex_types, np.array([2]).reshape(1,1)], axis=0 )
    elif +0<=z and z<=27: hex_types = np.concatenate( [hex_types, np.array([3]).reshape(1,1)], axis=0 )
    else:                 hex_types = np.concatenate( [hex_types, np.array([4]).reshape(1,1)], axis=0 )

#cubit.cmd('block 1 add hex all')
cubit.cmd('export abaqus "mesh.inp" dimension 3 overwrite cubitids')
cubit.cmd('export cubit "mesh.cub" overwrite')
pickle.dump( {'hex_ids':hex_ids,'hex_xyzs':hex_xyzs,'hex_types':hex_types}, open('mesh.pkl','wb') )
cubit.destroy()
