import sys
sys.path.append('../misc')
from header import *

class OptGD(Optimization):

  __mapper_args__ = {'polymorphic_identity':'GD'}

  def presample(self,args=None): return []

  def generate_sample(self,misc,args=None,runLocal=False):

    if 'objs' in args: objs = args['objs']
    else: objs = self.objectives

    session = sqlalchemy.inspect(self).session
    ant_obj=[]
    for relate in session.query(Relate).filter_by(relation='antecedent'):
      ant_obj  += [relate.sample_obj]
    nei_subj=[]
    nei_obj=[]
    for relate in session.query(Relate).filter_by(relation='neighbor'):
      nei_subj += [relate.sample_subj]
      nei_obj  += [relate.sample_obj]

    for sample in session.query(Sample).all():

      # if sample is a neighbor, pass
      if sample in nei_subj: continue

      # if sample has an antecedent, pass
      if sample in ant_obj: continue

      # if sample already has neighbors, check whether they are done
      if sample in nei_obj:
        done=1
        for relate in sample.subj_relates():
          if relate.relation=='neighbor':
            if relate.status()<2: done=0
        if sample.status()<2: done=0
        if done:
          # if neighbors are all done, compute gradient and make a step

          J = np.zeros([len(self.parameters),len(objs)],dtype='float')
          G = np.zeros([len(objs)],dtype='float')
          X = np.zeros([len(self.parameters)],dtype='float')

          for j in range(len(objs)):
            G[j] = sample.get_predictions(objs[j])[0].fetch_misfit()
            i=0
            for relate in sample.obj_relates():
              neighbor = relate.sample_subj
              x1 = neighbor.get_estimates(self.parameters[i])[0].value
              x2 = sample.get_estimates(self.parameters[i])[0].value
              y1 = neighbor.get_predictions(objs[j])[0].fetch_misfit()
              y2 = G[j]
              J[i,j] = (y2-y1)/(x2-x1)
              X[i] = sample.get_estimates(self.parameters[i])[0].value
              i+=1

          gradient = np.dot(J,G)
          gradient = gradient / np.linalg.norm(gradient)

          antecedent = sample.copy()
          for i in range(len(self.parameters)):
            antecedent.get_estimates(self.parameters[i])[0].value -= self.parameters[i].get_pxd().priorModel.step * gradient[i]
          antecedent.push(runLocal)
          relate = Relate( relation='antecedent', optimization=self, sample_subj=antecedent, sample_obj=sample )

          for parameter in self.parameters:
            neighbor = antecedent.copy()
            neighbor.get_estimates(parameter)[0].value += 0.01*parameter.get_pxd().priorModel.step
            neighbor.push(runLocal)
            relate = Relate( relation='neighbor', optimization=self, sample_subj=neighbor, sample_obj=antecedent )

    return []

  def create_chain(self,nn=1,runLocal=False):
    for i in range(nn):
      sample = Sample(optimization=self)
      self.setup_simulations(sample)
      for parameter in self.get_parameters():
        value    = parameter.get_pxd().priorModel.draw()
        estimate = Estimate(sample=sample,parameter=parameter,value=value)
        parameter.estimates.append(estimate)
      sample.misc = {'stepMod':1.0}
      sample.push(runLocal)

      for parameter in self.parameters:
        neighbor = sample.copy()
        neighbor.get_estimates(parameter)[0].value += 0.01*parameter.get_pxd().priorModel.step
        neighbor.push(runLocal)
        relate = Relate( relation='neighbor', optimization=self, sample_subj=neighbor, sample_obj=sample )
