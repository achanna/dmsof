import sys
sys.path.append('/home/ubuntu/poroelast9/imports')
sys.path.append('/home/ubuntu/poroelast9/imports/classes')
sys.path.append('/home/ubuntu/poroelast9/imports/functions')
sys.path.append('/home/ubuntu/poroelast9/imports/functions/misc')

import json

import numpy as np
import numpy.linalg
#import visit
#import cubit
import math
import random
import datetime
#from datetime import *
import pickle
import scipy
import scipy.io
import scipy.stats
import scipy.special
import scipy.linalg
import scipy.optimize
import scipy.interpolate

import itertools

import statsmodels
import statsmodels.nonparametric
import statsmodels.nonparametric.kernel_regression
import statsmodels.nonparametric.kernel_density

import shapely
import shapely.ops
import shapely.geometry

from sklearn.decomposition import PCA
import pyDOE
import functools

import jsonpickle
import paramiko
import cPickle
import time
import gc
import os
import os.path
import MySQLdb

import boto
import boto.s3
import boto.sqs
import boto.glacier
from boto.sqs.message import Message
from boto.s3.connection import S3Connection
from boto.s3.key import Key

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.collections
from matplotlib import cm
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patheffects as PathEffects

import matplotlib.patches
from matplotlib.patches import FancyArrowPatch

import pylab

from scipy.interpolate import interp1d
from scipy.interpolate import griddata

#import seaborn as sns

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.ext.mutable
from sqlalchemy import Table, Column, Integer, String, Binary, Float, Boolean, Enum, ForeignKey, PickleType, DateTime, LargeBinary
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy.types as types

from sqlalchemy.orm.session import Session

#from sqlalchemy.ext.declarative import declarative_base

from database_ops import *

from SOE_tables import *
from StatModel import *
from Gaussian import *
from Uniform import *

from OptGD import *
from OptMC import *
from OptSA import *
from OptMCMC import *
from OptMCMCrj1 import *
from OptSparse import *
from OptSimAnn import *
from OptEnKF import *
from OptNSGAII import *
from OptPareto import *
from OptSpecified import *
from OptLHC import *
from OptPCALHC import *

from OptNSGAII_pilot import *
from OptPareto_pilot import *
from OptSpecified_pilot import *
from OptSpecified_pilot2 import *

import forwardModels
import plotting_codes

'''import errorOperators

from Sample import *
#from Cycle import *

#from Population import *
#from Iteration import *

import geometry_builders
import forwardModels
import postProcessors
import interpMethods
import tradeoffs
import detrend
from generate_synthetic import *
from plotting_codes import *

from Optimization import *
from OptGD import *
from OptMCMC import *
from OptMCMCrj import *
from OptSPEA import *
from OptPost import *
from OptPostSparse import *
from OptSpecified import *
from OptResample import *
#from ForwardModel import *
#from Coordinator import *
from SOE_Database import *'''
