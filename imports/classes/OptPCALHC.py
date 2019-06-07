import sys
sys.path.append('../misc')
from header import *

class OptPCALHC(Optimization):

  __mapper_args__ = {'polymorphic_identity':'PCALHC'}

  def presample(self,args=None):
    nComps = 3
    paretoRanks = pickle.load(open('pareto.pkl','rb'))['paretoRank']
    parameters = self.get_parameters()

    ests=[]
    for sample in self.get_complete_samples():
      if paretoRanks[int(sample.id)]<=5:
        ests += [0]
        ests[-1] = [sample.get_estimates(param)[0].value for param in parameters]
    ests=np.array(ests)
    print ests
    print ests.shape
    print np.array([[np.min(ests[:,i]),np.max(ests[:,i])] for i in range(len(parameters))])

    pca = PCA(n_components=nComps)
    pca.fit(ests)

    x=pca.transform(ests)[:,0]
    y=pca.transform(ests)[:,1]
    z=pca.transform(ests)[:,2]
    xmin=np.min(x)
    xmax=np.max(x)
    ymin=np.min(y)
    ymax=np.max(y)
    zmin=np.min(z)
    zmax=np.max(z)

    ests = pyDOE.lhs( 3, samples=args['n'], criterion='corr' )
    ests[:,0] = xmin+(xmax-xmin)*ests[:,0]
    ests[:,1] = ymin+(ymax-ymin)*ests[:,1]
    ests[:,2] = zmin+(zmax-zmin)*ests[:,2]

    ests=pca.inverse_transform(ests)
    print ests
    print ests.shape
    print np.array([[np.min(ests[:,i]),np.max(ests[:,i])] for i in range(len(parameters))])
    exit()
    return {'ests':ests,'i':0}

  def generate_sample(self,misc,args=None,runLocal=False):
    sample = Sample(optimization=self)
    self.setup_simulations(sample)
    constraints = self.get_constraints()
    parameters = self.get_parameters()
    for j in range(len(parameters)):
      param = parameters[j]
      value = misc['ests'][misc['i'],j]
      estimate = Estimate(sample=sample,parameter=param,value=value)
      param.estimates.append(estimate)
    sample.push(runLocal)
    misc['i']+=1
    return []
