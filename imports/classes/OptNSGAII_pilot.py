import sys
sys.path.append('../misc')
from header import *

class OptNSGAII_pilot(Optimization):

  __mapper_args__ = {'polymorphic_identity':'NSGAII_pilot'}

  def startup(self):
    self.misc = {'dead_ids':[]}

  def presample(self,args=None):

    samplesComplete = self.get_complete_samples()

    print 'total complete samples', len(samplesComplete)

    #print self.misc
    #exit()
    #print len(self.misc['dead_ids']), len(np.unique(self.misc['dead_ids'])), min(self.misc['dead_ids']), max(self.misc['dead_ids'])

    samples=[]
    for sample in samplesComplete:
      if not sample.id in self.misc['dead_ids']:
        samples += [sample]

    print 'total live samples', len(samples)

    dobj=self.crowding_distances_obj(samples,args['objs'],logErr=True)

    candidates = samples[:]
    pop=[]
    fitness={}
    rank=1
    while len(pop)<args['N']:

      front=[]
      for isample in candidates:
        isPareto = True
        for jsample in candidates:
          if isample==jsample: continue
          ierrs = isample.get_errors(args['objs'])
          jerrs = jsample.get_errors(args['objs'])
          le = np.less_equal(jerrs,ierrs)
          lt = np.less(jerrs,ierrs)
          if np.all(le) and np.any(lt):
            isPareto = False
            break
        if isPareto:
          fitness[isample.id]=rank+(1-dobj[isample.id])
          front += [isample]
          candidates.remove(isample)
      if len(front)==0: break

      if (len(front)+len(pop))<=args['N']: pop += front
      else:
        dobjs = []
        for sample in front: dobjs += [dobj[sample.id]]
        ii = np.argsort(dobjs)

        for sample in np.array(front)[ii]: pop += [sample]
      rank+=1
    pop = pop[0:args['N']]

    #for sample in samples:
    #  if sample not in pop:
    #    self.misc['dead_ids'] += [sample.id]

    session = sqlalchemy.inspect(self).session
    session.commit()
    return {'pop':pop,'fitness':fitness}

  def crowding_distances_obj(self,samples,objs,logErr=False):

    errors = []
    for sample in samples:
      errors += [sample.get_errors(objs)]
    errors = np.array(errors)
    if logErr: errors = np.log10(errors)

    dists = np.zeros(errors.shape[0],dtype='float')
    for iObj in range(errors.shape[1]):
      for iSamp in range(errors.shape[0]):
        tErr = errors[iSamp,iObj]
        ilt  = np.where( errors[:,iObj]<errors[iSamp,iObj] )[0]
        igt  = np.where( errors[:,iObj]>errors[iSamp,iObj] )[0]
        if   len(ilt)>0 and len(igt)==0:
          lErr = np.max(errors[ilt,iObj])
          dists[iSamp] += 2*np.abs(lErr-tErr) / np.abs( np.max(errors[:,iObj])-np.min(errors[:,iObj]) )
        elif len(igt)>0 and len(ilt)==0:
          rErr = np.min(errors[igt,iObj])
          dists[iSamp] += 2*np.abs(rErr-tErr) / np.abs( np.max(errors[:,iObj])-np.min(errors[:,iObj]) )
        elif len(igt)==0 and len(ilt)==0:
          dists[iSamp]=0
        else:
          lErr = np.max(errors[ilt,iObj])
          rErr = np.min(errors[igt,iObj])
          dists[iSamp] += np.abs(rErr-lErr) / np.abs( np.max(errors[:,iObj])-np.min(errors[:,iObj]) )

    dists = dists / np.max(dists)
    output={}
    for i in range(len(samples)):
      output[samples[i].id] = dists[i]
    return output

  def crowding_distances_par(self,samples):

    values = []
    for sample in samples:
      values += [[]]
      for parameter in self.parameters:
        values[-1] += [sample.get_estimates(parameter)[0].value]
    values = np.reshape(np.array(values),[len(samples),len(self.parameters)])

    dists = np.zeros(values.shape[0],dtype='float')
    for iObj in range(values.shape[1]):
      for iSamp in range(values.shape[0]):
        tErr = values[iSamp,iObj]
        ilt  = np.where( values[:,iObj]<values[iSamp,iObj] )[0]
        igt  = np.where( values[:,iObj]>values[iSamp,iObj] )[0]
        if   len(ilt)>0 and len(igt)==0:
          lErr = np.max(values[ilt,iObj])
          dists[iSamp] += 2*np.abs(lErr-tErr) / np.abs( np.max(values[:,iObj])-np.min(values[:,iObj]) )
        elif len(igt)>0 and len(ilt)==0:
          rErr = np.min(values[igt,iObj])
          dists[iSamp] += 2*np.abs(rErr-tErr) / np.abs( np.max(values[:,iObj])-np.min(values[:,iObj]) )
        else:
          lErr = np.max(values[ilt,iObj])
          rErr = np.min(values[igt,iObj])
          dists[iSamp] += np.abs(rErr-lErr) / np.abs( np.max(values[:,iObj])-np.min(values[:,iObj]) )

    dists = dists / np.max(dists)
    output={}
    for i in range(len(samples)):
      output[samples[i].id] = dists[i]
    return output

  def generate_sample(self,misc,args=None,runLocal=False):

    pop     = misc['pop']
    fitness = misc['fitness']
    k       = args['tournament_size']

    tournament = np.random.choice(pop,k)
    fits = []
    bestFitness = 1e99
    for sample in tournament:
      if fitness[sample.id]<bestFitness:
        p1 = sample
        bestFitness = fitness[sample.id]

    tournament = np.random.choice(pop,k)
    fits = []
    bestFitness = 1e99
    for sample in tournament:
      if fitness[sample.id]<bestFitness:
        p2 = sample
        bestFitness = fitness[sample.id]

    sample = Sample(optimization=self)
    self.setup_simulations(sample)
    constraints = self.get_constraints()

    for parameter in self.get_parameters():
      estimate = Estimate(sample=sample,parameter=parameter,value=0)
      parameter.estimates.append(estimate)

    g1 = set(p1.misc)
    g2 = set(p2.misc)

    overlap = float(len(list(g1.intersection(g2)))) / float(len(list(g1.union(g2))))

    par1=[]
    par2=[]
    for estimate in p1.estimates: par1+=[estimate.value]
    for estimate in p2.estimates: par2+=[estimate.value]

    if g1==g2 or overlap>0.95:
      g3 = g1.union(g2)
      while True:
        for estimate in sample.estimates:
          p = np.random.choice([p1,p2])
          parentVal = p.get_estimates(estimate.parameter)[0].value
          var = estimate.parameter.get_pxd().priorModel.step
          estimate.value = np.random.normal(parentVal,var)
        if sample.is_within_bounds():
          if len(constraints)==0: break
          if np.all([constraint.fn(sample) for constraint in constraints]): break
    else:
      p3 = np.random.choice([p1,p2])
      g3 = set(p3.misc)
      if np.random.random()<0.5:
        # randomly add or subtract a random number (2-10) of border elements
        xyz  = pickle.load( open('mesh.pkl','rb') )['hex_xyzs']
        ii = np.where(np.multiply(xyz[:,2]>-5,xyz[:,2]<0))[0]
        xy = xyz[ii,0:2]
        vor = scipy.spatial.Voronoi(xy)

        nb_in=[]
        nb_out=[]
        for i in range(xy.shape[0]):
          ir = vor.point_region[i]
          iv = vor.regions[ir]
          v  = vor.vertices[iv]
          for j in range(xy.shape[0]):
            jr = vor.point_region[j]
            jv = vor.regions[jr]
            if not set(iv).isdisjoint(jv):
              if (i in g3) and not (j in g3):
                nb_in+=[i]
              if not (i in g3) and (j in g3):
                nb_out+=[i]

        '''plt.figure()
        for i in range(xy.shape[0]):
          ir = vor.point_region[i]
          iv = vor.regions[ir]
          v  = vor.vertices[iv]
          if -1 in iv: continue
          if i in nb_in:
            plt.fill(v[:,0],v[:,1],'orange',zorder=0,edgecolor='k',linewidth=0.3)
          if i in nb_out:
            plt.fill(v[:,0],v[:,1],'red',zorder=0,edgecolor='k',linewidth=0.3)
        plt.savefig('circ_mod1.eps',format='eps',bbox_inches='tight')
        plt.savefig('circ_mod1.png',format='png',bbox_inches='tight',dpi=300)
        plt.close()'''

        nb_change=[]
        if np.random.random()>0.5:
          chunk = np.random.randint(2,10)
          print 'lets add a %i element chunk to this circle' % chunk
          i = np.random.choice(nb_out)
          g3.add(i)

          for nn in range(chunk-1):
            nbs=[]
            ir = vor.point_region[i]
            iv = vor.regions[ir]
            v  = vor.vertices[iv]
            for j in range(xy.shape[0]):
              jr = vor.point_region[j]
              jv = vor.regions[jr]
              if not set(iv).isdisjoint(jv):
                if (i in g3) and not (j in g3):
                  nbs+=[j]
            if len(nbs)==0: return []
            i = np.random.choice(nbs)
            g3.add(i)
        else:
          chunk = np.random.randint(2,10)
          print 'lets lose a %i element chunk of this circle' % chunk
          i = np.random.choice(nb_in)
          g3.remove(i)
          for nn in range(chunk-1):
            nbs=[]
            ir = vor.point_region[i]
            iv = vor.regions[ir]
            v  = vor.vertices[iv]
            for j in range(xy.shape[0]):
              jr = vor.point_region[j]
              jv = vor.regions[jr]
              if not set(iv).isdisjoint(jv):
                if not (i in g3) and (j in g3):
                  nbs+=[j]
            if len(nbs)==0: return []
            i = np.random.choice(nbs)
            g3.remove(i)

        '''nb_in=[]
        nb_out=[]
        for i in range(xy.shape[0]):
          ir = vor.point_region[i]
          iv = vor.regions[ir]
          v  = vor.vertices[iv]
          for j in range(xy.shape[0]):
            jr = vor.point_region[j]
            jv = vor.regions[jr]
            if not set(iv).isdisjoint(jv):
              if (i in g3) and not (j in g3):
                nb_in+=[i]
              if not (i in g3) and (j in g3):
                nb_out+=[i]

        plt.figure()
        for i in range(xy.shape[0]):
          ir = vor.point_region[i]
          iv = vor.regions[ir]
          v  = vor.vertices[iv]
          if -1 in iv: continue
          if i in nb_in:
            plt.fill(v[:,0],v[:,1],'orange',zorder=0,edgecolor='k',linewidth=0.3)
          if i in nb_out:
            plt.fill(v[:,0],v[:,1],'red',zorder=0,edgecolor='k',linewidth=0.3)
        plt.savefig('circ_mod2.eps',format='eps',bbox_inches='tight')
        plt.savefig('circ_mod2.png',format='png',bbox_inches='tight',dpi=300)
        plt.close()'''

        for estimate in sample.estimates:
          parentVal = p3.get_estimates(estimate.parameter)[0].value
          estimate.value = parentVal

      else:
        while True:
          for estimate in sample.estimates:
            parentVal = p3.get_estimates(estimate.parameter)[0].value
            var = estimate.parameter.get_pxd().priorModel.step
            estimate.value = np.random.normal(parentVal,var)

          if sample.is_within_bounds():
            if len(constraints)==0: break
            if np.all([constraint.fn(sample) for constraint in constraints]): break

    sample.misc = list(g3)
    sample.push(runLocal)
    return [sample]
