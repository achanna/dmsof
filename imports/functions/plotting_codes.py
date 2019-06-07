import sys
sys.path.append('../misc')
from header import *
from connect_info import *

def plot_data(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None,bounds=None):

  print 'words go hurr'

  session = sqlalchemy.inspect(opts[0]).session

  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  if type(paretoRanks)==type(None):
    paretoRanks = update_pareto_rank_structure(opts,objectives)

  for objective in objectives:
    for meas in objective.measurements:

      #if (objective.id==4 or objective.id==5 or objective.id==6): continue
      #if (objective.id>9): continue
      print objective.id
      title_obj  = '%s [%s]' % (meas.instruments[0].title,meas.instruments[0].instType.unit)
      #if objective.id==1: title_obj = 'AVN2, EW Strain [$\mu \epsilon$]'
      #if objective.id==2: title_obj = 'AVN2, NS Strain [$\mu \epsilon$]'

      '''print 'data0', objective.id
      plt.figure()
      plt.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=3 )
      tmin = np.min( meas.indVars_actual )
      tmax = np.max( meas.indVars_actual )
      dmin = np.min( meas.data[:,1] )
      dmax = np.max( meas.data[:,1] )
      dt=(tmax-tmin)*0.03
      dd=(dmax-dmin)*0.03
      plt.xlim([tmin-dt,tmax+dt])
      plt.ylim([dmin-dd,dmax+dd])
#      if objective.id==1: plt.ylim([-50,400])
#      if objective.id==2: plt.ylim([-50,400])
      plt.savefig('%s/data0_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data0_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      plt.close()'''

      '''print 'data1', objective.id
      plt.figure()
      for opt in opts:
        for sample in opt.samples:
          if sample.status()==2:
            for prediction in sample.get_predictions(objective):
              indVars = meas.indVars_prescribed
              data    = prediction.data
              if type(data)!=type(None):
                plt.plot( indVars, data, c=[0.75,0.75,0.75], zorder=2 )
#      if objective.id==1: plt.ylim([-50,400])
#      if objective.id==2: plt.ylim([-50,400])
      plt.savefig('%s/data1_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data1_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      plt.close()'''

      '''print 'data2', objective.id
      plt.figure()
      for opt in opts:
        for sample in opt.samples:
          if sample.status()==2:
            for prediction in sample.get_predictions(objective):
              if type(prediction.data)!=type(None):
                indVars,data = meas.detrend(prediction)
                plt.plot( indVars, data, c=[0.75,0.75,0.75], zorder=2 )
      plt.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=3 )
      tmin = np.min( meas.indVars_actual )
      tmax = np.max( meas.indVars_actual )
      dmin = np.min( meas.data[:,1] )
      dmax = np.max( meas.data[:,1] )
      dt=(tmax-tmin)*0.03
      dd=(dmax-dmin)*0.03
      plt.xlim([tmin-dt,tmax+dt])
      plt.ylim([dmin-dd,dmax+dd])
#      if objective.id==1: plt.ylim([-50,400])
#      if objective.id==2: plt.ylim([-50,400])
      plt.savefig('%s/data2_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data2_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      plt.close()'''

      '''print 'data3', objective.id
      bestErr=1e99
      plt.figure()
      dmin = +np.inf
      dmax = -np.inf
      for opt in opts:
        for sample in opt.samples:
          if sample.status()==2:
            for prediction in sample.get_predictions(objective):
              if type(prediction.data)!=type(None):
                indVars,data = meas.detrend(prediction)
                plt.plot( indVars, data, c=[0.75,0.75,0.75], zorder=0 )
                if np.min(data)<dmin: dmin=np.min(data)
                if np.max(data)>dmax: dmax=np.max(data)
                err = prediction.fetch_misfit()
                if err<bestErr and type(err)!=type(None):
                  bestErr = err
                  best    = prediction
      indVars,data = meas.detrend(best)
      plt.plot( indVars, data, c='b', linewidth=3, zorder=1 )
      plt.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=2 )

      tmin = np.min( meas.indVars_actual )
      tmax = np.max( meas.indVars_actual )
      dt=(tmax-tmin)*0.03
      dd=(dmax-dmin)*0.03
      plt.xlim([tmin-dt,tmax+dt])
      plt.ylim([dmin-dd,dmax+dd])
#      plt.ylim([0,160])
#      if objective.id==1: plt.ylim([-40,140])
#      if objective.id==2: plt.ylim([-100,15])
      plt.xlabel( 'Time [days]',    fontsize=32 )
      plt.ylabel( '%s' % title_obj, fontsize=32 )
#      if objective.id==1: plt.ylim([-50,400])
#      if objective.id==2: plt.ylim([-50,400])
      plt.savefig('%s/data3_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data3_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      dmin = np.min( meas.data )
      dmax = np.max( meas.data )
      dt=(tmax-tmin)*0.03
      dd=(dmax-dmin)*0.03
      plt.xlim([tmin-dt,tmax+dt])
      plt.ylim([dmin-dd,dmax+dd])
      plt.savefig('%s/data3b_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data3b_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      plt.close()'''

      '''print 'data4', objective.id
      plt.figure()
      cols = ['r','g','b','c']
      labs = ['731:+200','4A:+200','1A:-1500','25-1W:+400']
      pos  = ['upper left','lower left','upper left']
      smin=+1e99
      smax=-1e99
      for isig in range(len(best.signals)):
        si  = best.signals[isig].data
        si *= 1e9
        si -= si[0]
        si = np.append( 0,si )
        if np.min(si)<smin: smin=np.min(si)
        if np.max(si)>smax: smax=np.max(si)
        plt.plot( indVars, si, c=cols[isig], label=labs[isig], zorder=0 )
      indVars,data = meas.detrend(best)
      plt.plot( indVars, data, c='k', label='Best', zorder=1 )
      plt.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', label='Measured', zorder=2 )
      tmin = np.min( meas.indVars_actual )
      tmax = np.max( meas.indVars_actual )
      dmin = np.min( meas.data )
      dmax = np.max( meas.data )
      dmin = np.min([ dmin, smin ])
      dmin = np.min([ dmin, smax ])
      dmin = np.min([ dmin, np.min(data) ])
      dmax = np.max([ dmax, np.max(data) ])
      dt = (tmax-tmin)*0.03
      dd = (dmax-dmin)*0.03
      plt.xlim([tmin-dt,tmax+dt])
      plt.ylim([dmin-dd,dmax+dd])
      plt.legend(loc=pos[objective.id-1])
      plt.savefig('%s/data4_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data4_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      plt.close()'''

      '''print 'data5', objective.id
      plt.figure()
      dmin = np.min( meas.data )
      dmax = np.max( meas.data )
      for opt in opts:
        for sample in opt.samples:
          if sample.status()==2:
            for prediction in sample.get_predictions(objective):
              if type(prediction.data)!=type(None):
                indVars,data = meas.detrend(prediction)
                plt.plot( indVars, data, c=[0.75,0.75,0.75], zorder=0 )
                if np.min(data)<dmin: dmin=np.min(data)
                if np.max(data)>dmax: dmax=np.max(data)
      rnkd_samps=[]
      rnks=[]
      for opt in opts:
        for sample in opt.samples:
          if sample.status()==2:
            rnkd_samps += [sample]
            rnks       += [paretoRanks[sample.id]]
      ii = np.where(np.array(rnks)==1)[0]
      for sample in np.array(rnkd_samps)[ii]:
        for prediction in sample.get_predictions(objective):
          indVars,data = meas.detrend(prediction)
          plt.plot( indVars, data, c='k', zorder=1 )
      plt.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=2 )
      tmin = np.min( meas.indVars_actual )
      tmax = np.max( meas.indVars_actual )
      dmin = np.min( meas.data )
      dmax = np.max( meas.data )
      dt=(tmax-tmin)*0.03
      dd=(dmax-dmin)*0.03
      plt.xlim([tmin-dt,tmax+dt])
      plt.ylim([dmin-dd,dmax+dd])
      plt.xlabel( 'Time [days]',    fontsize=32 )
      plt.ylabel( '%s' % title_obj, fontsize=32 )
      plt.savefig('%s/data5_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data5_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      plt.close()'''

      '''print 'data6', objective.id
      plt.figure()

      for opt in opts:
        for sample in opt.samples:
          if sample.status()==2:
            for prediction in sample.get_predictions(objective):
              if type(prediction.data)!=type(None):
                indVars,data = meas.detrend(prediction)
                plt.plot( indVars, data, c=[0.75,0.75,0.75], zorder=0 )

      rnkd_samps=[]
      rnks=[]
      for opt in opts:
        for sample in opt.samples:
          if sample.status()==2:
            rnkd_samps += [sample]
            rnks       += [paretoRanks[sample.id]]

      for obj in objectives:
        if obj.id==1:
          break

      paretoSamples=[]
      paretoObj1=[]
      ii = np.where(np.array(rnks)==1)[0]
      for sample in np.array(rnkd_samps)[ii]:
        prediction     = sample.get_predictions(obj)[0]
        paretoObj1    += [prediction.fetch_misfit()]
        paretoSamples += [sample]

      ii = np.argsort(paretoObj1)
      print ii
      for sample in np.array(paretoSamples)[ii]:
        print sample, sample.get_predictions(objectives[0])[0].fetch_misfit(), sample.get_predictions(objectives[1])[0].fetch_misfit()
        for parameter in opts[0].parameters:
          for estimate in sample.get_estimates(parameter):
            print parameter.property.title, estimate.value

      prediction = paretoSamples[ii[0]].get_predictions(objective)[0]
      indVars,data = meas.detrend(prediction)
      plt.plot( indVars, data, c='b', label='Best EW fit', linewidth=2, zorder=1 )

      prediction = paretoSamples[ii[-1]].get_predictions(objective)[0]
      indVars,data = meas.detrend(prediction)
      plt.plot( indVars, data, c='orange', label='Best NS fit', linewidth=2, zorder=1 )

      label=1
      ii = [ii[4],ii[5],ii[6],ii[7]]
      for sample in np.array(paretoSamples)[np.array(ii)]:
        prediction = sample.get_predictions(objective)[0]
        indVars,data = meas.detrend(prediction)
        if label==1:
          plt.plot( indVars, data, c='k', label='Middle ground', linewidth=2, zorder=1 )
          label = 0
        else:
          plt.plot( indVars, data, c='k', linewidth=2, zorder=1 )

      plt.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=2 )
      tmin = np.min( meas.indVars_actual )
      tmax = np.max( meas.indVars_actual )
      dmin = np.min( meas.data )
      dmax = np.max( meas.data )
      dt=(tmax-tmin)*0.03
      dd=(dmax-dmin)*0.03
      plt.xlim([tmin-dt,tmax+dt])
#      plt.ylim([dmin-dd,dmax+dd])
#      if objective.id==1: plt.ylim([-40,140])
#      if objective.id==2: plt.ylim([-100,15])
      plt.xlabel( 'Time [days]',    fontsize=32 )
      plt.ylabel( '%s' % title_obj, fontsize=32 )
      if objective.id==1: plt.legend(loc=2)
      if objective.id==2: plt.legend(loc=3)
      plt.savefig('%s/data6_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data6_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      plt.close()'''

      '''print 'data7', objective.id
      plt.figure()
      dmin = +np.inf
      dmax = -np.inf
      for opt in opts:
        for sample in opt.samples:
          if sample.status()==2:
            for prediction in sample.get_predictions(objective):
              if type(prediction.data)!=type(None):
                indVars,data = meas.detrend(prediction)
                plt.plot( indVars, data, c=[0.75,0.75,0.75], zorder=0 )

                if np.min(data)<dmin: dmin=np.min(data)
                if np.max(data)>dmax: dmax=np.max(data)

                if paretoRanks[sample.id]<2:

                  if len(sample.get_predictions(objectives[0]))==1:
                    if len(sample.get_predictions(objectives[1]))==1:
#                      if sample.get_predictions(objectives[0])[0].fetch_misfit() < 10:
#                        if sample.get_predictions(objectives[1])[0].fetch_misfit() < 8:
                          print sample.id
                          indVars,data = meas.detrend(prediction)
                          plt.plot( indVars, data, c='k', linewidth=2, zorder=1 )

      plt.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=2 )
      tmin = np.min( meas.indVars_actual )
      tmax = np.max( meas.indVars_actual )
      dt=(tmax-tmin)*0.03
      dd=(dmax-dmin)*0.03
      plt.xlim([tmin-dt,tmax+dt])
      plt.ylim([dmin-dd,dmax+dd])
      plt.xlabel( 'Time [days]',    fontsize=32 )
      plt.ylabel( '%s' % title_obj, fontsize=32 )
      plt.savefig('%s/data7_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data7_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      dmin = np.min( meas.data )
      dmax = np.max( meas.data )
      dt=(tmax-tmin)*0.03
      dd=(dmax-dmin)*0.03
      plt.xlim([tmin-dt,tmax+dt])
      plt.ylim([dmin-dd,dmax+dd])
      plt.savefig('%s/data7b_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data7b_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      plt.close()'''

      print 'data8', objective.id
      plt.figure()
      dmin = +np.inf
      dmax = -np.inf
      dmin1 = +np.inf
      dmax1 = -np.inf
      count = 0
      bestErr=1e99
      for opt in opts:
        for sample in opt.samples:
          if sample.status()==2:
            for prediction in sample.get_predictions(objective):
              if type(prediction.data)!=type(None):
                indVars,data = meas.detrend(prediction)
                plt.plot( indVars, data, c=[0.75,0.75,0.75], zorder=0 )

                err = prediction.fetch_misfit()
                if err<bestErr and type(err)!=type(None):
                  bestErr = err
                  best    = prediction

                if paretoRanks[sample.id]<50:

                  if len(sample.get_predictions(objectives[0]))==1:
                    if len(sample.get_predictions(objectives[1]))==1:
                      exx = sample.get_predictions(objectives[0])[0].fetch_misfit()
                      eyy = sample.get_predictions(objectives[1])[0].fetch_misfit()
                      ezz = sample.get_predictions(objectives[2])[0].fetch_misfit()
                      #pf1 = sample.get_predictions(objectives[6])[0].fetch_misfit()
                      #pf2 = sample.get_predictions(objectives[7])[0].fetch_misfit()
                      #pf3 = sample.get_predictions(objectives[8])[0].fetch_misfit()
                      #pf1,pf2,pf3=0,0,0

                      # 137
                      #k1 = sample.get_estimates(opts[0].parameters[0])[0].value
                      #k2 = sample.get_estimates(opts[0].parameters[7])[0].value
                      #k3 = sample.get_estimates(opts[0].parameters[5])[0].value

                      # 144
                      #k1 = sample.get_estimates(opts[0].parameters[4])[0].value
                      #k2 = sample.get_estimates(opts[0].parameters[11])[0].value
                      #k3 = sample.get_estimates(opts[0].parameters[0])[0].value

                      # 145
                      #k1 = sample.get_estimates(opts[0].parameters[4])[0].value
                      #k2 = sample.get_estimates(opts[0].parameters[13])[0].value
                      #k3 = sample.get_estimates(opts[0].parameters[0])[0].value

                      # 157
                      #k1 = sample.get_estimates(opts[0].parameters[8])[0].value
                      #k2 = sample.get_estimates(opts[0].parameters[10])[0].value
                      #k3 = sample.get_estimates(opts[0].parameters[7])[0].value

                      # 169
                      k1 = sample.get_estimates(opts[0].parameters[6])[0].value
                      k2 = sample.get_estimates(opts[0].parameters[7])[0].value
                      k3 = sample.get_estimates(opts[0].parameters[3])[0].value

                      if exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2]:
                      #if k1>k2 and k2>k3 and k3<-16 and \
                      #  exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] and \
                      #  pf1<bounds[3] and pf2<bounds[4] and pf3<bounds[5]:
                      #if True:
                          count+=1
                          print sample.id
                          indVars,data = meas.detrend(prediction)
                          plt.plot( indVars, data, c='k', linewidth=2, zorder=1 )
                          if np.min(data)<dmin1: dmin1=np.min(data)
                          if np.max(data)>dmax1: dmax1=np.max(data)

      #if (objective.id==5 or objective.id==6): pass
      #else:
      if True:
        #indVars,data = meas.detrend(best)
        #plt.plot( indVars, data, c='b', linewidth=3, zorder=2 )
        plt.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=3 )

      tmin = np.min( meas.indVars_actual )
      tmax = np.max( meas.indVars_actual )
      if np.min(meas.data[:,1])<dmin1: dmin1=np.min(meas.data[:,1])
      if np.max(meas.data[:,1])>dmax1: dmax1=np.max(meas.data[:,1])
      dmin = dmin1
      dmax = dmax1
      dt=(tmax-tmin)*0.03
      dd=(dmax-dmin)*0.03

      plt.xlim([tmin-dt,tmax+dt])
      plt.ylim([dmin-dd,dmax+dd])
      plt.savefig('%s/data8_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data8_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      dt=(tmax-tmin)*0.03
      dd=(dmax-dmin)*0.03

      plt.xlabel( 'Time [days]',    fontsize=32 )
      plt.ylabel( '%s' % title_obj, fontsize=32 )
      plt.xlim([tmin-dt,tmax+dt])
      plt.ylim([dmin-dd,dmax+dd])
      plt.savefig('%s/data8b_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data8b_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
      plt.close()

def plot_data_SA(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None):

  session = sqlalchemy.inspect(opts[0]).session

  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  parameters = session.query(Parameter).order_by(Parameter.id).all()

  if type(paretoRanks)==type(None):
    paretoRanks = update_pareto_rank_structure(opts,objectives)

  ii=0
  for parameter in parameters:
    plt.figure()
    for objective in objectives:
      for meas in objective.measurements:
        new=1
        values=[]
        misfits=[]
        for sample in opts[0].samples[ii:ii+100]:
          if sample.status()==2:
            for prediction in sample.get_predictions(objective):
              if type(prediction.data)!=type(None):
                values  += [sample.get_estimates(parameter)[0].value]
                misfits += [prediction.fetch_misfit()]

      if objective.id==1: title_obj = 'AVN2, NS Strain [$\mu \epsilon$]'
      if objective.id==2: title_obj = 'AVN2, EW Strain [$\mu \epsilon$]'
      if objective.id==1: plt.scatter(values,misfits,s=20,c='r',edgecolor='none',label=title_obj)
      if objective.id==2: plt.scatter(values,misfits,s=20,c='b',edgecolor='none',label=title_obj)
    plt.legend()
    plt.savefig('%s/surf_%s_par%02i.eps' % (plotdir,fn_suffix,parameter.id), format='eps', bbox_inches='tight' )
    plt.savefig('%s/surf_%s_par%02i.png' % (plotdir,fn_suffix,parameter.id), format='png', bbox_inches='tight', dpi=300 )
    plt.close()
    ii+=100

  for objective in objectives:
    for meas in objective.measurements:

      zmin = np.min(meas.data[:,1])
      zmax = np.max(meas.data[:,1])
      for sample in opts[0].samples:
        if sample.status()==2:
          for prediction in sample.get_predictions(objective):
            if type(prediction.data)!=type(None):
              indVars,data = meas.detrend(prediction)
              if np.min(data)<zmin: zmin=np.min(data)
              if np.max(data)>zmax: zmax=np.max(data)

      ii=0
      for parameter in parameters:

        pxd=parameter.get_pxd()
        title_obj  = '%s [%s]' % (meas.instruments[0].title,meas.instruments[0].instType.unit)
        if objective.id==1: title_obj = 'AVN2, NS Strain [$\mu \epsilon$]'
        if objective.id==2: title_obj = 'AVN2, EW Strain [$\mu \epsilon$]'

        vmin = parameter.get_pxd().priorModel.min
        vmax = parameter.get_pxd().priorModel.max
        norm = mpl.colors.Normalize( vmin=vmin, vmax=vmax )
        cmap = cm.ScalarMappable( norm=norm, cmap=mpl.cm.jet_r )

        plt.figure()
        v=np.linspace(vmin,vmax,100)
        sc=plt.scatter(v,v,s=10,c=v,cmap=mpl.cm.jet_r)
        plt.close()

        print 'data8', objective.id, parameter.id
        plt.figure()
        for sample in opts[0].samples[ii:ii+100]:
          if sample.status()==2:
            for prediction in sample.get_predictions(objective):
              if type(prediction.data)!=type(None):
                value=sample.get_estimates(parameter)[0].value
                indVars,data = meas.detrend(prediction)
                plt.plot( indVars, data, c=cmap.to_rgba(value), zorder=0 )

        plt.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='k', edgecolor='none', marker='.', zorder=2 )

        plt.colorbar(sc)
        title = '%s %s [%s]' % (pxd.domain.title,pxd.property.title,pxd.property.unit)
        plt.title(title, fontsize=32)
        tmin = np.min( meas.indVars_actual )
        tmax = np.max( meas.indVars_actual )
        dt=(tmax-tmin)*0.03
        dz=(zmax-zmin)*0.03
        plt.xlim([tmin-dt,tmax+dt])
        plt.ylim([zmin-dz,zmax+dz])
        plt.xlabel( 'Time [days]',    fontsize=32 )
        plt.ylabel( '%s' % title_obj, fontsize=32 )
        plt.savefig('%s/data8_%s_obj%02i_par%02i.eps' % (plotdir,fn_suffix,objective.id,parameter.id), format='eps', bbox_inches='tight' )
        plt.savefig('%s/data8_%s_obj%02i_par%02i.png' % (plotdir,fn_suffix,objective.id,parameter.id), format='png', bbox_inches='tight', dpi=600 )
        plt.close()
        ii+=100


def plot_data_chains(opts,plotdir,fn_suffix,objectives=None):
  opts[0].get_chains()
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))
  for objective in objectives:
    plt.figure()
    for chain in opts[0].get_chains():
      t=[]
      e=[]
      for sample in chain:
        for simulation in sample.simulations:
          for prediction in simulation.predictions:
            if prediction.objective==objective:
              t.append( simulation.outputFileEndTime.strftime("%s") )
              e.append( prediction.fetch_misfit() )
      plt.plot(t,np.log10(e))
    plt.savefig('%s/data_chains_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
    plt.savefig('%s/data_chains_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )

def plot_data_chains_frames(opts,plotdir,fn_suffix,nFrames,objectives=None):
  chains = opts[0].get_chains()
#  chains = [chains[0]]
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))
  tMin = +1e99
  tMax = -1e99
  eMin = +1e99
  eMax = -1e99
  for opt in opts:
    for sample in opt.samples:
      if sample.status()==2:
        for simulation in sample.simulations:
          for prediction in simulation.predictions:
            ti = sample.id
            ei = prediction.fetch_misfit()
            if ti<tMin: tMin=ti
            if ti>tMax: tMax=ti
            if ei<eMin: eMin=ei
            if ei>eMax: eMax=ei
  dt=0.02*(tMax-tMin)
  de=0.02*(eMax-eMin)
  tLims = np.linspace(tMin,tMax,nFrames)
  for objective in objectives:
    for iFrame in range(1,nFrames):
      print 'Plotting frame %i' % iFrame

      V = np.linspace(-0.5,+0.5,100)
      plt.figure()
      cmap = plt.get_cmap('coolwarm')
      sc = plt.scatter( V, V, c=V, cmap=cmap)
      plt.clf()
      cNorm  = colors.Normalize( vmin=np.min(V), vmax=np.max(V) )
      scalarMap = cm.ScalarMappable(norm=cNorm, cmap=cmap)
      plt.close()

      plt.subplot(3,1,1)
      for chain in chains:
        t=[]
        e=[]
        for sample in chain:
          for simulation in sample.simulations:
            for prediction in simulation.predictions:
              if prediction.objective==objective:
                ti = sample.id
                if ti<tLims[iFrame]:
                  t.append( ti )
                  e.append( prediction.fetch_misfit() )
        plt.semilogy(t,e,c=[0.6,0.6,0.6])
      plt.plot([tMin-dt,tMax+dt],[130.458,130.458],'--',c='r')
      plt.xlim([tMin-dt,tMax+dt])
      plt.ylim([eMin-de,eMax+de])
      plt.ylim([100,np.ceil(eMax+de)])

      plt.subplot(3,1,2)
      best = chains[0][0]
      bestErr = +1e99
      for chain in chains:
        for sample in chain:
          for simulation in sample.simulations:
            ti = sample.id
            if ti<tLims[iFrame]:
              for prediction in simulation.predictions:
                if prediction.objective==objective:
                  ei = prediction.fetch_misfit()
                  if ei<bestErr:
                    best=sample
                    bestErr=ei
                  indVars = prediction.objective.instrument.indVars
                  data    = prediction.predicted
                  plt.plot( indVars, data, c=[0.8,0.8,0.8], linewidth=0.5, zorder=1 )
        plt.plot( indVars, data, c=[0.4,0.4,0.4], linewidth=1.0, zorder=2 )
      for simulation in best.simulations:
        for prediction in simulation.predictions:
          if prediction.objective==objective:
            indVars = prediction.objective.instrument.indVars
            data    = prediction.predicted
            plt.plot( indVars, data, c='b', linewidth=1.75, zorder=3 )
      plt.scatter( objective.measurement.observed[:,0], objective.measurement.observed[:,1], s=15, c='r', edgecolor='none', marker='o', zorder=4 )
      plt.xlim([np.min(objective.instrument.indVars),np.max(objective.instrument.indVars)])

      plt.subplot(3,1,3)
      x = np.linspace(-100,100,200)
      y = np.linspace(-100,0,100)
      X,Y = np.meshgrid(x,y)
      V = np.zeros(X.shape)
      errTotal = 0
      for chain in chains:
        for sample in chain:
          ti = sample.id
          if ti<tLims[iFrame]:
            errTotal += sample.likelihood_unnormalized()
            V        += sample.likelihood_unnormalized() * sample.interp_model_to_grid((X,Y))
      V /= errTotal
      ticks = np.linspace(-0.5, 0.5, 10, endpoint=True)
      plt.contourf(X,Y,V,200,cmap=plt.get_cmap('coolwarm'),vmin=-0.5,vmax=+0.5)
      plt.clim([-0.5,+0.5])
      plt.colorbar( sc, orientation='horizontal' )

#      plt.savefig('%s/data_chains_%s_obj%02i_frame%04i.eps' % (plotdir,fn_suffix,objective.id,iFrame), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data_chains_%s_obj%02i_frame%04i.png' % (plotdir,fn_suffix,objective.id,iFrame), format='png', bbox_inches='tight', dpi=100 )
      plt.close()

def plot_data_chains_frames2(opts,plotdir,fn_suffix,nFrames,objectives=None):
  chains = opts[0].get_chains()
#  chains = [chains[0]]
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))
  tMin = +1e99
  tMax = -1e99
  eMin = +1e99
  eMax = -1e99
  for opt in opts:
    for sample in opt.samples:
      if sample.status()==2:
        for simulation in sample.simulations:
          for prediction in simulation.predictions:
            ti = sample.id
            ei = prediction.fetch_misfit()
            if ti<tMin: tMin=ti
            if ti>tMax: tMax=ti
            if ei<eMin: eMin=ei
            if ei>eMax: eMax=ei
  dt=0.02*(tMax-tMin)
  de=0.02*(eMax-eMin)
  tLims = np.linspace(tMin,tMax,nFrames)
  for objective in objectives:
    for iFrame in range(1,nFrames):
      print 'Plotting frame %i' % iFrame

      plt.subplot(1,1,1)
      best = chains[0][0]
      bestErr = +1e99
      for chain in chains:
        for sample in chain:
          for simulation in sample.simulations:
            ti = sample.id
            if ti<tLims[iFrame]:
              for prediction in simulation.predictions:
                if prediction.objective==objective:
                  ei = prediction.fetch_misfit()
                  if ei<bestErr:
                    best=sample
                    bestErr=ei
                  indVars = prediction.objective.instrument.indVars
                  data    = prediction.predicted
                  plt.plot( indVars, data, c=[0.8,0.8,0.8], linewidth=0.5, zorder=1 )
        plt.plot( indVars, data, c=[0.4,0.4,0.4], linewidth=1.0, zorder=2 )
      for simulation in best.simulations:
        for prediction in simulation.predictions:
          if prediction.objective==objective:
            indVars = prediction.objective.instrument.indVars
            data    = prediction.predicted
            plt.plot( indVars, data, c='b', linewidth=1.75, zorder=3 )
      plt.scatter( objective.measurement.observed[:,0], objective.measurement.observed[:,1], s=15, c='r', edgecolor='none', marker='o', zorder=4 )
      plt.xlim([np.min(objective.instrument.indVars),np.max(objective.instrument.indVars)])

#      plt.savefig('%s/data_chains_%s_obj%02i_frame%04i.eps' % (plotdir,fn_suffix,objective.id,iFrame), format='eps', bbox_inches='tight' )
      plt.savefig('%s/data2_chains_%s_obj%02i_frame%04i.png' % (plotdir,fn_suffix,objective.id,iFrame), format='png', bbox_inches='tight', dpi=100 )
      plt.close()

def plot_sigsq(opts,plotdir,fn_suffix,objectives=None):
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))
  for objective in objectives:
    fig, ax1 = plt.subplots()
    errs=[]
    for opt in opts:
      for sample in opt.samples:
        if sample.status()==2:
          for simulation in sample.simulations:
            for simulation in sample.simulations:
              for prediction in simulation.predictions:
                if prediction.objective==objective:
                  errs.append(np.log10(prediction.fetch_misfit()))
    errs = np.array(errs)
    sigsq = np.log10(objective.measurement.sigsq)
    n, bins, patches = ax1.hist(errs, 50, facecolor='green')
    ax1.plot( [sigsq,sigsq], [0,np.max(n)], '--', c='k' )
    ax1.set_xlim([1,7])
    ax1.set_ylim([0,np.max(n)])
    ax1.set_xlabel('$\sigma^2_n$',fontsize=18)
    ax1.set_ylabel('Number samples',fontsize=18)
    ax1.tick_params('y', colors='k')

    e=np.log10(objective.measurement.sigsq)
    w=2.65
    a=26.0
    x = np.linspace(0,7,1000)
    t = (x-e*0.90)/w
    pdf = 1.0/(2.0*math.pi)**0.5 * np.exp(-t**2.0/2.0)
    cdf = (1.0+scipy.special.erf((t*a)/2.0**0.5))/2.0
    p   = 2.0 / w * pdf * cdf
    p  /= np.max(p)

    sigsq = objective.measurement.sigsq
    p2  = (2*math.pi*sigsq)**-0.5 * np.exp(-0.5 * 10**x / sigsq )
    p2 /= np.max(p2)

    ax2 = ax1.twinx()
    ax2.plot(x,p)
    ax2.plot(x,p2)
    ax2.set_xlim([1,7])
    ax2.set_ylim([0,1.07])
    ax2.set_ylabel('$L(\sigma^2)$', color='b')
    ax2.tick_params('y', colors='b')

    plt.savefig('%s/sigsq_%s_obj%02i.eps' % (plotdir,fn_suffix,objective.id), format='eps', bbox_inches='tight' )
    plt.savefig('%s/sigsq_%s_obj%02i.png' % (plotdir,fn_suffix,objective.id), format='png', bbox_inches='tight', dpi=600 )
    plt.close()

def plot_pxd2d(opts,plotdir,fn_suffix,objectives=None,parameter_pairs=None):
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))
  if type(parameter_pairs)==type(None):
    session = sqlalchemy.inspect(opts[0]).session
    parameters=session.query(Parameter).all()
    parameter_pairs = list(itertools.combinations(parameters,2))

  samples = opts[0].get_complete_samples()
  for obj in objectives:
    for meas in obj.measurements:
      v=[]
      for sample in samples:
        v.append(sample.get_predictions(obj)[0].fetch_misfit())

      for ipar,jpar in list(itertools.combinations(parameters,2)):
        print obj.id, ipar.id, jpar.id
        title_obj  = '%s [%s]' % (meas.instruments[0].title,meas.instruments[0].instType.unit)
        title_ipar = '%s %s [%s]' % (ipar.get_pxd().domain.title,ipar.get_pxd().property.title,ipar.get_pxd().property.unit)
        title_jpar = '%s %s [%s]' % (jpar.get_pxd().domain.title,jpar.get_pxd().property.title,jpar.get_pxd().property.unit)
        rng_ipar   = [ipar.get_pxd().priorModel.min,ipar.get_pxd().priorModel.max]
        rng_jpar   = [jpar.get_pxd().priorModel.min,jpar.get_pxd().priorModel.max]

        x=[]
        y=[]
        for sample in samples:
          x.append(sample.get_estimates(ipar)[0].value)
          y.append(sample.get_estimates(jpar)[0].value)

        '''plt.figure()
        plt.scatter(x,y,s=20,c=v,edgecolor='none')
        plt.xlabel( '%s' % title_ipar, fontsize=22)
        plt.ylabel( '%s' % title_jpar, fontsize=22)
        plt.title(  '%s' % title_obj,  fontsize=24)
        plt.tick_params(axis='both', which='major', labelsize=18)
        plt.xlim(rng_ipar)
        plt.ylim(rng_jpar)
        plt.colorbar()
        plt.savefig('%s/errors_%s_pxd%02i_pxd%02i_obj%02i.eps'%(plotdir,fn_suffix,ipar.id,jpar.id,obj.id),format='eps',bbox_inches='tight' )
        plt.savefig('%s/errors_%s_pxd%02i_pxd%02i_obj%02i.png'%(plotdir,fn_suffix,ipar.id,jpar.id,obj.id),format='png',bbox_inches='tight', dpi=600 )
        plt.close()'''

        '''mu = np.mean(np.log10(v))
        sg = np.var(np.log10(v))**0.5
        plt.figure()
        plt.hist(np.log10(v),bins=20)
        ylim = plt.gca().get_ylim()
        plt.plot([np.min(np.log10(v)),np.min(np.log10(v))],ylim,'k--')
        plt.plot([mu+sg,mu+sg],ylim,'k--')
        plt.savefig('%s/errors_%s_hist_pxd%02i_pxd%02i_obj%02i.eps'%(plotdir,fn_suffix,ipar.id,jpar.id,obj.id),format='eps',bbox_inches='tight' )
        plt.savefig('%s/errors_%s_hist_pxd%02i_pxd%02i_obj%02i.png'%(plotdir,fn_suffix,ipar.id,jpar.id,obj.id),format='png',bbox_inches='tight', dpi=600 )
        plt.close()'''

        plt.figure()
        plt.scatter(x,y,s=20,c=np.log10(v),edgecolor='none')
        plt.xlabel( '%s' % title_ipar, fontsize=22)
        plt.ylabel( '%s' % title_jpar, fontsize=22)
        plt.title(  '%s' % title_obj,  fontsize=24)
        plt.tick_params(axis='both', which='major', labelsize=18)
        plt.xlim(rng_ipar)
        plt.ylim(rng_jpar)
        #plt.clim([ np.min(np.log10(v)), mu+sg ])
        plt.colorbar()
        plt.savefig('%s/errors_%s_log_pxd%02i_pxd%02i_obj%02i.eps'%(plotdir,fn_suffix,ipar.id,jpar.id,obj.id),format='eps',bbox_inches='tight' )
        plt.savefig('%s/errors_%s_log_pxd%02i_pxd%02i_obj%02i.png'%(plotdir,fn_suffix,ipar.id,jpar.id,obj.id),format='png',bbox_inches='tight', dpi=600 )
        plt.close()

def plot_pareto2d(opts,plotdir,fn_suffix,objectives=None,parameter_pairs=None,paretoRanks=None):
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))
  if type(parameter_pairs)==type(None):
    session = sqlalchemy.inspect(opts[0]).session
    parameters=session.query(Parameter).all()
    parameter_pairs = list(itertools.combinations(parameters,2))

  samples = opts[0].get_complete_samples()
  for obj in objectives:
    for meas in obj.measurements:
      v=[]
      for sample in samples:
        try: v.append(sample.get_predictions(obj)[0].fetch_misfit())
        except: pass

      rnk=[]
      for sample in samples:
        try: rnk += [paretoRanks[sample.id]]
        except: pass

      for ipar,jpar in list(itertools.combinations(parameters,2)):
        print obj.id, ipar.id, jpar.id
        title_obj  = '%s [%s]' % (meas.instruments[0].title,meas.instruments[0].instType.unit)
        title_ipar = '%s %s [%s]' % (ipar.get_pxd().domain.title,ipar.get_pxd().property.title,ipar.get_pxd().property.unit)
        title_jpar = '%s %s [%s]' % (jpar.get_pxd().domain.title,jpar.get_pxd().property.title,jpar.get_pxd().property.unit)
        rng_ipar   = [ipar.get_pxd().priorModel.min,ipar.get_pxd().priorModel.max]
        rng_jpar   = [jpar.get_pxd().priorModel.min,jpar.get_pxd().priorModel.max]

        x=[]
        y=[]
        for sample in samples:
          x.append(sample.get_estimates(ipar)[0].value)
          y.append(sample.get_estimates(jpar)[0].value)

        plt.figure()
        plt.scatter(x,y,s=20,c=rnk,edgecolor='none')
        plt.xlabel( '%s' % title_ipar, fontsize=22)
        plt.ylabel( '%s' % title_jpar, fontsize=22)
        plt.title(  '%s' % title_obj,  fontsize=24)
        plt.tick_params(axis='both', which='major', labelsize=18)
        plt.xlim(rng_ipar)
        plt.ylim(rng_jpar)
        plt.xlim([rng_ipar[0],10**8.4])
        plt.ylim([rng_jpar[0],10**8.4])
        plt.colorbar()
        plt.savefig('%s/pareto_%s_pxd%02i_pxd%02i_obj%02i.eps'%(plotdir,fn_suffix,ipar.id,jpar.id,obj.id),format='eps',bbox_inches='tight' )
        plt.savefig('%s/pareto_%s_pxd%02i_pxd%02i_obj%02i.png'%(plotdir,fn_suffix,ipar.id,jpar.id,obj.id),format='png',bbox_inches='tight', dpi=600 )
        plt.close()

def plot_pxd2d_coin(opts,plotdir,fn_suffix,objectives=None):
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  parameters = opts[0].get_parameters()
  samples = opts[0].get_complete_samples()
  for obj in objectives:
    eMax=0
    for sample in samples:
      for prediction in sample.get_predictions(obj):
        print prediction
        e = np.log10(prediction.fetch_misfit())
        if e>eMax: eMax=e
    print eMax

    e0=[]
    for sample in samples:
      for prediction in sample.get_predictions(obj):
        e = np.log10(prediction.fetch_misfit())
        if e<eMax: e0.append( e )
    norm = mpl.colors.Normalize( vmin=np.min(e0), vmax=np.max(e0) )
    cmap = cm.ScalarMappable( norm=norm, cmap=mpl.cm.jet_r )
    plt.figure()
    sc=plt.scatter( e0, e0, c=e0, cmap=mpl.cm.jet_r )
    plt.close()

    fig,ax = plt.subplots()
    for sample in samples:
      for prediction in sample.get_predictions(obj):
        for est in sample.estimates:
          if   est.parameter.property.abv=='cx': x0 = est.value
          elif est.parameter.property.abv=='cy': y0 = est.value
          elif est.parameter.property.abv=='lr': r0 = est.value
        e0 = np.log10(prediction.fetch_misfit())
        if e0<eMax:
          c=plt.Circle( (x0,y0), r0, color=cmap.to_rgba(e0), fill=False, zorder=-e0 )
          ax.add_artist(c)
    cb = plt.colorbar(sc)
    plt.xlim([-1000,+5000])
    plt.ylim([-1000,+5000])
    plt.savefig('%s/errors_coin_%s_obj%02i.eps'%(plotdir,fn_suffix,obj.id),format='eps',bbox_inches='tight' )
    plt.savefig('%s/errors_coin_%s_obj%02i.png'%(plotdir,fn_suffix,obj.id),format='png',bbox_inches='tight', dpi=600 )
    plt.close()

def plot_pareto_coin(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None,bounds=None):
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  samples = opts[0].get_complete_samples()

  fig,ax = plt.subplots()
  patches=[]
  for sample in samples:
    for est in sample.estimates:
      if   est.parameter.property.abv=='cx': x0 = est.value
      elif est.parameter.property.abv=='cy': y0 = est.value
      elif est.parameter.property.abv=='lr': r0 = est.value
    if paretoRanks[sample.id]<50:
      exx = sample.get_predictions(objectives[0])[0].fetch_misfit()
      eyy = sample.get_predictions(objectives[1])[0].fetch_misfit()
      ezz = sample.get_predictions(objectives[2])[0].fetch_misfit()
      pf1 = sample.get_predictions(objectives[6])[0].fetch_misfit()
      pf2 = sample.get_predictions(objectives[7])[0].fetch_misfit()
      pf3 = sample.get_predictions(objectives[8])[0].fetch_misfit()
      #if exx<8 and eyy<12 and ezz<12:
      #  if pf1<5 and pf2<11 and pf3<8:
      #if exx<10 and eyy<15 and ezz<15:
      #if pf1<25 and pf2<30 and pf3<35:

      # 137
      #k1 = sample.get_estimates(opts[0].parameters[0])[0].value
      #k2 = sample.get_estimates(opts[0].parameters[7])[0].value
      #k3 = sample.get_estimates(opts[0].parameters[5])[0].value

      # 144
      k1 = sample.get_estimates(opts[0].parameters[4])[0].value
      k2 = sample.get_estimates(opts[0].parameters[11])[0].value
      k3 = sample.get_estimates(opts[0].parameters[0])[0].value

      # 145
      #k1 = sample.get_estimates(opts[0].parameters[4])[0].value
      #k2 = sample.get_estimates(opts[0].parameters[13])[0].value
      #k3 = sample.get_estimates(opts[0].parameters[0])[0].value

      # 157
      #k1 = sample.get_estimates(opts[0].parameters[8])[0].value
      #k2 = sample.get_estimates(opts[0].parameters[10])[0].value
      #k3 = sample.get_estimates(opts[0].parameters[7])[0].value

      if k1>k2 and k2>k3 and k3<-16 and \
        exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] and \
        pf1<bounds[3] and pf2<bounds[4] and pf3<bounds[5]:

          #if sample.get_errors([objectives[0]])[0]<7 and sample.get_errors([objectives[1]])[0]<5 and sample.get_errors([objectives[2]])[0]<5:
          #if sample.get_errors([objectives[0]])[0]<10 and sample.get_errors([objectives[1]])[0]<16 and sample.get_errors([objectives[2]])[0]<16:
          #if sample.get_errors([objectives[6]])[0]<4000 and sample.get_errors([objectives[7]])[0]<50:

          c=matplotlib.patches.Circle( (x0,y0), r0, fc=(1,0,0,0), ec='gray', lw=0.5, zorder=0 )
          ax.add_artist(c)
          print x0,y0,r0

      #c=matplotlib.patches.Circle( (-200,-20), 250, fc=(1,0,0,0), ec='blue', lw=3, zorder=1 )
      #ax.add_artist(c)
      #print x0,y0,r0

      #e=matplotlib.patches.Ellipse( (-60,-20), 2*1200, 2*640, angle=27, fc=(1,0,0,0), ec='red', lw=2, zorder=0 )
      #ax.add_artist(e)

  '''plt.scatter( 0,0, s=20, c='r')
  plt.scatter( +239.8,  -75.3, s=20, c='b')
  #plt.scatter( +374.6, -199.1, s=20, c='b')
  plt.scatter( -375.9,   -5.4, s=20, c='b')
  plt.scatter( -185.0,  +28.7, s=20, c='b')
  plt.scatter( -245.0, -111.7, s=20, c='b')

  plt.text(   +0.0,   +0.0, '9A')
  plt.text( -39.650,  +426.447, 'AVN2')
  #plt.text( +374.6, -199.1, '11A')
  plt.text( -375.9,   -5.4, '27')
  plt.text( -185.0,  +28.7, '29')
  plt.text( -245.0, -111.7, '60')'''

  '''xx=[-290.36,+204.16,+789.80,-789.80]
  yy=[-410.66,+92.75,+418.56,-163.44]

  xx0=-39.650328056
  yy0=+426.44735133

  plt.scatter( xx[0], yy[0], s=20, c='r', zorder=1 )
  plt.scatter( xx[1], yy[1], s=20, c='g', zorder=1 )
  plt.scatter( xx[2], yy[2], s=20, c='b', zorder=1 )
  plt.scatter( xx[3], yy[3], s=20, c='c', zorder=1 )
  plt.scatter( xx0, yy0, s=20, c='m', zorder=1 )

  plt.text( xx[0], yy[0], '731', zorder=1 )
  plt.text( xx[1], yy[1], '4A', zorder=1 )
  plt.text( xx[2], yy[2], '1A', zorder=1 )
  plt.text( xx[3], yy[3], '25-1W', zorder=1 )
  plt.text(   xx0,   yy0, 'AVN2', zorder=1 )

  plt.xlim([-1400,+1000])
  plt.ylim([-1200,+1200])'''

  xy = np.array([	[ +239.8,  -75.3, +515.0 ],
			[ +206.8,  -60.5, +495.0 ],
			[ +374.6, -199.1,   -3.0 ],
			[ -375.9,   -5.4,   -3.0 ],
			[ -185.0,  +28.7,   -3.0 ],
			[ -245.0, -111.7,   -3.0 ],
			[   +0.0,   -0.0,   -3.0 ] ], dtype='float')

  plt.scatter( xy[0,0], xy[0,1], s=20, c='r', zorder=1 )
  #plt.scatter( xy[1,0], xy[1,1], s=20, c='r', zorder=1 )
  #plt.scatter( xy[2,0], xy[2,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[3,0], xy[3,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[4,0], xy[4,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[5,0], xy[5,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[6,0], xy[6,1], s=20, c='r', zorder=1 )

  plt.scatter( 993.2164321933, -83.5660275454, s=20, c='r', zorder=1 )

  plt.text( xy[0,0], xy[0,1], 'AVN2')
  #plt.text( xy[1,0], xy[1,1], 'AVN3')
  #plt.text( xy[2,0], xy[2,1], '11A')
  plt.text( xy[3,0], xy[3,1], '27')
  plt.text( xy[4,0], xy[4,1], '29')
  plt.text( xy[5,0], xy[5,1], '60')
  plt.text( xy[6,0], xy[6,1], '9A')

  #plt.text( 993.2164321933, -83.5660275454, '1A' )

  plt.xlim([-750,+500])
  plt.ylim([-625,+625])
  plt.xlabel('Easting [m]',fontsize=18)
  plt.ylabel('Northing [m]',fontsize=18)
  plt.savefig('%s/errors_coin_pareto_%s.eps'%(plotdir,fn_suffix),format='eps',bbox_inches='tight' )
  plt.savefig('%s/errors_coin_pareto_%s.png'%(plotdir,fn_suffix),format='png',bbox_inches='tight', dpi=600 )
  plt.close()

def plot_pareto_ellipse(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None,bounds=None):
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  samples = opts[0].get_complete_samples()

  fig,ax = plt.subplots()
  patches=[]
  for sample in samples:
    for est in sample.estimates:
      if   est.parameter.property.abv=='cx': x0 = est.value
      elif est.parameter.property.abv=='cy': y0 = est.value
      elif est.parameter.property.abv=='el': el = est.value
      elif est.parameter.property.abv=='ew': ew = est.value
      elif est.parameter.property.abv=='ea': ea = est.value

    if paretoRanks[sample.id]<50:
      exx = sample.get_predictions(objectives[0])[0].fetch_misfit()
      eyy = sample.get_predictions(objectives[1])[0].fetch_misfit()
      ezz = sample.get_predictions(objectives[2])[0].fetch_misfit()
      pf1 = sample.get_predictions(objectives[6])[0].fetch_misfit()
      pf2 = sample.get_predictions(objectives[7])[0].fetch_misfit()
      pf3 = sample.get_predictions(objectives[8])[0].fetch_misfit()
      #if exx<8 and eyy<12 and ezz<12:
      #  if pf1<5 and pf2<11 and pf3<8:
      #if exx<10 and eyy<15 and ezz<15:
      #if pf1<25 and pf2<30 and pf3<35:

      # 137
      #k1 = sample.get_estimates(opts[0].parameters[0])[0].value
      #k2 = sample.get_estimates(opts[0].parameters[7])[0].value
      #k3 = sample.get_estimates(opts[0].parameters[5])[0].value

      # 144
      k1 = sample.get_estimates(opts[0].parameters[4])[0].value
      k2 = sample.get_estimates(opts[0].parameters[11])[0].value
      k3 = sample.get_estimates(opts[0].parameters[0])[0].value

      # 145
      k1 = sample.get_estimates(opts[0].parameters[4])[0].value
      k2 = sample.get_estimates(opts[0].parameters[13])[0].value
      k3 = sample.get_estimates(opts[0].parameters[0])[0].value

      # 157
      #k1 = sample.get_estimates(opts[0].parameters[8])[0].value
      #k2 = sample.get_estimates(opts[0].parameters[10])[0].value
      #k3 = sample.get_estimates(opts[0].parameters[7])[0].value

      if k1>k2 and k2>k3 and k3<-16 and \
        exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] and \
        pf1<bounds[3] and pf2<bounds[4] and pf3<bounds[5]:

          #if sample.get_errors([objectives[0]])[0]<7 and sample.get_errors([objectives[1]])[0]<5 and sample.get_errors([objectives[2]])[0]<5:
          #if sample.get_errors([objectives[0]])[0]<10 and sample.get_errors([objectives[1]])[0]<16 and sample.get_errors([objectives[2]])[0]<16:
          #if sample.get_errors([objectives[6]])[0]<4000 and sample.get_errors([objectives[7]])[0]<50:

          e=matplotlib.patches.Ellipse( (x0,y0), el, ew, angle=ea, fc=(1,0,0,0), ec='gray', lw=0.5, zorder=0 )
          ax.add_artist(e)
          print x0,y0,el,ew,ea

  '''xy = np.array([	[ +239.8,  -75.3, +515.0 ],
			[ +206.8,  -60.5, +495.0 ],
			[ +374.6, -199.1,   -3.0 ],
			[ -375.9,   -5.4,   -3.0 ],
			[ -185.0,  +28.7,   -3.0 ],
			[ -245.0, -111.7,   -3.0 ],
			[   +0.0,   -0.0,   -3.0 ] ], dtype='float')

  plt.scatter( xy[0,0], xy[0,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[1,0], xy[1,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[2,0], xy[2,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[3,0], xy[3,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[4,0], xy[4,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[5,0], xy[5,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[6,0], xy[6,1], s=20, c='r', zorder=1 )

  plt.text( xy[0,0], xy[0,1], 'AVN2')
  plt.text( xy[1,0], xy[1,1], 'AVN3')
  plt.text( xy[2,0], xy[2,1], '11A')
  plt.text( xy[3,0], xy[3,1], '27')
  plt.text( xy[4,0], xy[4,1], '29')
  plt.text( xy[5,0], xy[5,1], '60')
  plt.text( xy[6,0], xy[6,1], '9A')'''


  xy = np.array([	[ +239.8,  -75.3, +515.0 ],
			[ +206.8,  -60.5, +495.0 ],
			[ +374.6, -199.1,   -3.0 ],
			[ -375.9,   -5.4,   -3.0 ],
			[ -185.0,  +28.7,   -3.0 ],
			[ -245.0, -111.7,   -3.0 ],
			[   +0.0,   -0.0,   -3.0 ] ], dtype='float')

  plt.scatter( xy[0,0], xy[0,1], s=20, c='r', zorder=1 )
  #plt.scatter( xy[1,0], xy[1,1], s=20, c='r', zorder=1 )
  #plt.scatter( xy[2,0], xy[2,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[3,0], xy[3,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[4,0], xy[4,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[5,0], xy[5,1], s=20, c='r', zorder=1 )
  plt.scatter( xy[6,0], xy[6,1], s=20, c='r', zorder=1 )

  plt.scatter( 993.2164321933, -83.5660275454, s=20, c='r', zorder=1 )

  plt.text( xy[0,0], xy[0,1], 'AVN2')
  #plt.text( xy[1,0], xy[1,1], 'AVN3')
  #plt.text( xy[2,0], xy[2,1], '11A')
  plt.text( xy[3,0], xy[3,1], '27')
  plt.text( xy[4,0], xy[4,1], '29')
  plt.text( xy[5,0], xy[5,1], '60')
  plt.text( xy[6,0], xy[6,1], '9A')

  #plt.text( 993.2164321933, -83.5660275454, '1A' )

  plt.xlim([-750,+500])
  plt.ylim([-625,+625])
  plt.xlabel('Easting [m]',fontsize=18)
  plt.ylabel('Northing [m]',fontsize=18)
  plt.savefig('%s/errors_ellipse_pareto_%s.eps'%(plotdir,fn_suffix),format='eps',bbox_inches='tight' )
  plt.savefig('%s/errors_ellipse_pareto_%s.png'%(plotdir,fn_suffix),format='png',bbox_inches='tight', dpi=600 )
  plt.close()

def plot_pareto_coin2(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None):

  x = np.array([ 1240.51, 1732.51, 1278.04, 1298.09, 1263.04, 1581.36, 1881.96, 1872.36, 1938.88, 3034.81, 2563.26, 2690.65])
  y = np.array([ 2951.18, 2897.22, 1971.61, 2249.13, 2166.77, 1032.7, 1776.19, 1847.41, 1924.94, 2340.91, 2488.6, 2341.580])
  r = np.array([ 1323.34, 1259.29, 1224.79, 1355.63, 1416.58, 1472.26, 626.121, 871.004, 817.936, 1172.55, 1299.51, 1257.51])

  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  if type(paretoRanks)==type(None):
    paretoRanks = update_pareto_rank_structure(opts,objectives)
  samples = opts[0].get_complete_samples()

  fig,ax = plt.subplots()
  for sample in samples:
    for est in sample.estimates:
      if   est.parameter.property.abv=='cx': x0 = est.value
      elif est.parameter.property.abv=='cy': y0 = est.value
      elif est.parameter.property.abv=='lr': r0 = est.value
    c=plt.Circle( (x0,y0), r0, color=[0.75,0.75,0.75], fill=False, zorder=0 )
    ax.add_artist(c)

  c=plt.Circle( (x[0],y[0]), r[0], color='b', linewidth=2, fill=False )
  ax.add_artist(c)

  c=plt.Circle( (x[-1],y[-1]), r[-1], color='orange', linewidth=2, fill=False )
  ax.add_artist(c)

  for i in range(4,8):
    c=plt.Circle( (x[i],y[i]), r[i], color='k', linewidth=2, fill=False )
    ax.add_artist(c)

  plt.xlim([-1000,+5000])
  plt.ylim([-1000,+5000])
  plt.xlabel('Easting [m]',fontsize=28)
  plt.ylabel('Northing [m]',fontsize=28)
  plt.savefig('%s/errors_coin2_pareto_%s.eps'%(plotdir,fn_suffix),format='eps',bbox_inches='tight' )
  plt.savefig('%s/errors_coin2_pareto_%s.png'%(plotdir,fn_suffix),format='png',bbox_inches='tight', dpi=600 )
  plt.close()

def plot_pareto(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None):
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  instx  = objectives[0].measurements[0].instruments[0]
  insty  = objectives[1].measurements[0].instruments[0]
  titlex = '%s %s [%s]' % (instx.title,instx.instType.abv,instx.instType.unit)
  titley = '%s %s [%s]' % (insty.title,insty.instType.abv,insty.instType.unit)

  if type(paretoRanks)==type(None):
    paretoRanks = update_pareto_rank_structure(opts,objectives[0:2])

  errs=np.zeros([0,2],dtype='float')
  rnks=[]
  for opt in opts:
    for sample in opt.samples:
      if sample.status()==2:
        errs  = np.vstack([ errs, np.array(sample.get_errors(objectives[0:2])).reshape([1,2]) ])
        rnks += [paretoRanks[sample.id]]

  ii = np.where(np.array(rnks)==1)[0]

  exMin = np.sort(errs[:,0])[0]
  eyMin = np.sort(errs[:,1])[0]
  exMax = np.sort(errs[:,0])[-3]
  eyMax = np.sort(errs[:,1])[-3]
  dx    = 0.02*(np.log10(exMax)-np.log10(exMin))
  dy    = 0.02*(np.log10(eyMax)-np.log10(eyMin))

  exMin = 10**(np.log10(exMin)-dx)
  eyMin = 10**(np.log10(eyMin)-dy)
  exMax = 10**(np.log10(exMax)+dx)
  eyMax = 10**(np.log10(eyMax)+dy)

  rank1 = errs[ii,:]
  ii = np.argsort(rank1[:,0])
  rank1 = rank1[ii]

  fig,ax = plt.subplots()
  plt.plot( rank1[:,0], rank1[:,1], linewidth=2, c=[0.7,0.7,0.7], zorder=0 )
  sc=plt.scatter( errs[:,0], errs[:,1], s=30, c=rnks, edgecolor='none', zorder=1 )

  plt.xlabel( '%s' % titlex, fontsize=22)
  plt.ylabel( '%s' % titley, fontsize=22)

  plt.xlabel( 'Misfit, EW Strain [$\mu\epsilon$]', fontsize=32)
  plt.ylabel( 'Misfit, NS Strain [$\mu\epsilon$]', fontsize=32)

  plt.xlim([ exMin, exMax ])
  plt.ylim([ eyMin, eyMax ])
  plt.xlim([ 10**4.6,10**8.5 ])
  plt.ylim([ 10**4.2,10**7.8 ])
  ax.set_xscale("log", nonposx='clip')
  ax.set_yscale("log", nonposx='clip')
  cb = plt.colorbar(sc)
  cb.set_label('Pareto Rank',fontsize=32)
  plt.savefig('%s/pareto.eps'%plotdir,format='eps',bbox_inches='tight' )
  plt.savefig('%s/pareto.png'%plotdir,format='png',bbox_inches='tight', dpi=600 )
  plt.close()

def plot_pareto2(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None):

#  other_errs  = pickle.load(open('../72/pareto.pkl','rb'))['errs']
#  other_errs /= 3500.0

  par_x = np.linspace(0,5,1000)
  par_y = np.linspace(0,5,1000)

  par_f1 = 4*par_x**2 + 4*par_y**2
  par_f2 = (par_x-5)**2 + (par_y-5)**2

  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  instx  = objectives[0].measurements[0].instruments[0]
  insty  = objectives[1].measurements[0].instruments[0]
  titlex = '%s %s [%s]' % (instx.title,instx.instType.abv,instx.instType.unit)
  titley = '%s %s [%s]' % (insty.title,insty.instType.abv,insty.instType.unit)

  if type(paretoRanks)==type(None):
    paretoRanks = update_pareto_rank_structure(opts,objectives[0:2])

  errs=np.zeros([0,2],dtype='float')
  rnks=[]
  for opt in opts:
    for sample in opt.samples:
      print sample.id, len(opt.samples)
      if sample.status()==2:
        try:
          errs  = np.vstack([ errs, np.array(sample.get_errors(objectives[0:2])).reshape([1,2]) ])
          rnks += [paretoRanks[sample.id]]
        except: pass

#  ii = np.where(np.array(rnks)==1)[0]

  exMin = np.sort(errs[:,0])[0]
  eyMin = np.sort(errs[:,1])[0]
  exMax = np.sort(errs[:,0])[-3]
  eyMax = np.sort(errs[:,1])[-3]
  dx    = 0.02*(np.log10(exMax)-np.log10(exMin))
  dy    = 0.02*(np.log10(eyMax)-np.log10(eyMin))

  exMin = 10**(np.log10(exMin)-dx)
  eyMin = 10**(np.log10(eyMin)-dy)
  exMax = 10**(np.log10(exMax)+dx)
  eyMax = 10**(np.log10(eyMax)+dy)

#  rank1 = errs[ii,:]
#  ii = np.argsort(rank1[:,0])
#  rank1 = rank1[ii]

  fig,ax = plt.subplots()

#  plt.plot( par_f1, par_f2, 'k--', linewidth=1, zorder=0 )

#  plt.plot( rank1[:,0], rank1[:,1], linewidth=2, c=[0.7,0.7,0.7], zorder=1 )

#  plt.scatter( other_errs[:,0], other_errs[:,1], s=30, c=[0.6,0.6,0.6], edgecolor='none', zorder=2 )
  print np.min(errs[:,0]), np.max(errs[:,0])
  print np.min(errs[:,1]), np.max(errs[:,1])
#  sc=plt.scatter( errs[:,0], errs[:,1], s=10, c=[0.6,0.6,0.6], edgecolor='none', zorder=3 )
  sc=plt.scatter( errs[:,0], errs[:,1], s=10, c=rnks, edgecolor='none', zorder=3 )

  plt.xlabel( '%s' % titlex, fontsize=22)
  plt.ylabel( '%s' % titley, fontsize=22)

#  plt.xlabel( 'Misfit, EW Strain [$n\epsilon$]', fontsize=32)
#  plt.ylabel( 'Misfit, NS Strain [$n\epsilon$]', fontsize=32)

#  plt.xlim([ exMin, exMax ])
#  plt.ylim([ eyMin, eyMax ])
#  plt.xlim([ 10**4.2,10**8.3 ])
#  plt.ylim([ 10**4.2,10**8.3 ])
#  plt.xlim([ 1e-2,1e+1 ])
#  plt.ylim([ 1e-2,1e+1 ])
#  plt.xlim([ 1e+4,1e+8 ])
#  plt.ylim([ 1e+4,1e+8 ])

#  plt.xlim([ 1.0e-2, 1.0e+1 ])
#  plt.ylim([ 1.0e-2, 1.0e+1 ])

  ax.set_xscale("log", nonposx='clip')
  ax.set_yscale("log", nonposx='clip')
  if np.max(rnks)>12:
    ticks = np.linspace(1,np.max(rnks),8)
    ticks = range(1,30,8)
    ticks = np.round(ticks)
    cb = plt.colorbar(sc,ticks=ticks)
    plt.clim(1,30)
  else:
    cb = plt.colorbar(sc)
  cb.set_label('Pareto Rank',fontsize=32)
  plt.savefig('%s/pareto2.eps'%plotdir,format='eps',bbox_inches='tight' )
  plt.savefig('%s/pareto2.png'%plotdir,format='png',bbox_inches='tight', dpi=600 )

  ax.set_xscale("linear")
  ax.set_yscale("linear")
  plt.xlim([ 5, 10 ])
  plt.ylim([ 3, 8 ])
  plt.savefig('%s/pareto2_inset.eps'%plotdir,format='eps',bbox_inches='tight' )
  plt.savefig('%s/pareto2_inset.png'%plotdir,format='png',bbox_inches='tight', dpi=600 )

  plt.close()

def plot_pareto3b(opts,plotdir,fn_suffix,objectives=None,paretoRanksFixed=None,bounds=None):

  for i in range(len(objectives)):

    if type(paretoRanksFixed)==type(None):
      paretoRanks = start_pareto_rank_structure(opts,objectives[i])
    else:
      paretoRanks = paretoRanksFixed

    print objectives[i]
    instx  = objectives[i][0].measurements[0].instruments[0]
    insty  = objectives[i][1].measurements[0].instruments[0]
    titlex = '%s %s [%s]' % (instx.title,instx.instType.abv,instx.instType.unit)
    titley = '%s %s [%s]' % (insty.title,insty.instType.abv,insty.instType.unit)

    exMin = +np.inf
    exMax = -np.inf
    eyMin = +np.inf
    eyMax = -np.inf
    errs=np.zeros([0,2],dtype='float')
    rnks=[]
    optids=[]
    sampids = []
    j=0
    jj=[]
    for opt in opts:
      for sample in opt.samples:
        print sample.id, len(opt.samples)
        if sample.status()==2:
          try:
            # 137
            #k1 = sample.get_estimates(opts[0].parameters[0])[0].value
            #k2 = sample.get_estimates(opts[0].parameters[7])[0].value
            #k3 = sample.get_estimates(opts[0].parameters[5])[0].value

            # 144
            #k1 = sample.get_estimates(opts[0].parameters[4])[0].value
            #k2 = sample.get_estimates(opts[0].parameters[11])[0].value
            #k3 = sample.get_estimates(opts[0].parameters[0])[0].value

            # 145
            #k1 = sample.get_estimates(opts[0].parameters[4])[0].value
            #k2 = sample.get_estimates(opts[0].parameters[13])[0].value
            #k3 = sample.get_estimates(opts[0].parameters[0])[0].value

            # 157
            #k1 = sample.get_estimates(opts[0].parameters[8])[0].value
            #k2 = sample.get_estimates(opts[0].parameters[10])[0].value
            #k3 = sample.get_estimates(opts[0].parameters[7])[0].value

            # 169
            k1 = sample.get_estimates(opts[0].parameters[6])[0].value
            k2 = sample.get_estimates(opts[0].parameters[7])[0].value
            k3 = sample.get_estimates(opts[0].parameters[3])[0].value

            errs     = np.vstack([ errs, np.array(sample.get_errors(objectives[i])).reshape([1,2]) ])
            rnks    += [paretoRanks[sample.id]]
            optids  += [int(opt.id)]
            sampids += [int(sample.id)]

            #print k1, k2, k3
            if k1>k2 and k2>k3:
              jj+=[j]
            j+=1
          except: pass

    dx = (exMax-exMin)*0.03
    dy = (eyMax-eyMin)*0.03

    fig,ax = plt.subplots()

    sc=plt.scatter( errs[:,0], errs[:,1], s=10, c=[0.6,0.6,0.6], edgecolor='none', zorder=3 )
    sc=plt.scatter( errs[np.array(jj),0], errs[np.array(jj),1], s=10, c=np.array(rnks)[np.array(jj)], edgecolor='none', zorder=4 )

    cb=plt.colorbar(sc)
    cb.set_label('Pareto Rank',fontsize=18)
    plt.xlabel( '%s' % titlex, fontsize=22)
    plt.ylabel( '%s' % titley, fontsize=22)

    plt.xlim([ 0.1, 1000 ])
    plt.ylim([ 0.1, 1000 ])

    ax.set_xscale("log", nonposx='clip')
    ax.set_yscale("log", nonposx='clip')
    plt.savefig('%s/pareto3b_%s_obj%02i_obj%02i.eps'%(plotdir,fn_suffix,objectives[i][0].id,objectives[i][1].id),format='eps',bbox_inches='tight' )
    plt.savefig('%s/pareto3b_%s_obj%02i_obj%02i.png'%(plotdir,fn_suffix,objectives[i][0].id,objectives[i][1].id),format='png',bbox_inches='tight', dpi=600 )

    if objectives[i][0].id==1: plt.xlim( bounds[0] )
    if objectives[i][0].id==2: plt.xlim( bounds[1] )
    if objectives[i][0].id==3: plt.xlim( bounds[2] )
    if objectives[i][0].id==7: plt.xlim( bounds[3] )
    if objectives[i][0].id==8: plt.xlim( bounds[4] )
    if objectives[i][0].id==9: plt.xlim( bounds[5] )

    if objectives[i][1].id==1: plt.ylim( bounds[0] )
    if objectives[i][1].id==2: plt.ylim( bounds[1] )
    if objectives[i][1].id==3: plt.ylim( bounds[2] )
    if objectives[i][1].id==7: plt.ylim( bounds[3] )
    if objectives[i][1].id==8: plt.ylim( bounds[4] )
    if objectives[i][1].id==9: plt.ylim( bounds[5] )

    plt.savefig('%s/pareto3b_%s_inset_obj%02i_obj%02i.png'%(plotdir,fn_suffix,objectives[i][0].id,objectives[i][1].id),format='png',bbox_inches='tight', dpi=600 )

    plt.close()

def plot_pareto3c(opts,plotdir,fn_suffix,objectives=None,paretoRanksFixed=None,bounds=None):

  for i in range(len(objectives)):

    if type(paretoRanksFixed)==type(None):
      paretoRanks = start_pareto_rank_structure(opts,objectives[i])
    else:
      paretoRanks = paretoRanksFixed

    print objectives[i]
    instx  = objectives[i][0].measurements[0].instruments[0]
    insty  = objectives[i][1].measurements[0].instruments[0]
    titlex = '%s %s [%s]' % (instx.title,instx.instType.abv,instx.instType.unit)
    titley = '%s %s [%s]' % (insty.title,insty.instType.abv,insty.instType.unit)

    exMin = +np.inf
    exMax = -np.inf
    eyMin = +np.inf
    eyMax = -np.inf
    errs=np.zeros([0,2],dtype='float')
    rnks=[]
    optids=[]
    sampids = []
    for opt in opts:
      for sample in opt.samples:
        print sample.id, len(opt.samples)
        if sample.status()==2:
          try:

            # 137
            k1 = sample.get_estimates(opts[0].parameters[0])[0].value
            k2 = sample.get_estimates(opts[0].parameters[7])[0].value
            k3 = sample.get_estimates(opts[0].parameters[5])[0].value

            #if k1>k2 and k2>k3:
            errs     = np.vstack([ errs, np.array(sample.get_errors(objectives[i])).reshape([1,2]) ])
            rnks    += [sample.id]
            optids  += [int(opt.id)]
            sampids += [int(sample.id)]
            #if paretoRanks[sample.id]:
            #  if errs[-1,0]<exMin: exMin = errs[-1,0]
            #  if errs[-1,0]>exMax: exMax = errs[-1,0]
            #  if errs[-1,1]<eyMin: eyMin = errs[-1,1]
            #  if errs[-1,1]>eyMax: eyMax = errs[-1,1]
          except: pass

    dx = (exMax-exMin)*0.03
    dy = (eyMax-eyMin)*0.03

    fig,ax = plt.subplots()

    sc=plt.scatter( errs[:,0], errs[:,1], s=10, c=rnks, edgecolor='none', zorder=3 )

    cb=plt.colorbar(sc)
    cb.set_label('Pareto Rank',fontsize=18)
    plt.xlabel( '%s' % titlex, fontsize=22)
    plt.ylabel( '%s' % titley, fontsize=22)

    plt.xlim([ 0.1, 1000 ])
    plt.ylim([ 0.1, 1000 ])

    ax.set_xscale("log", nonposx='clip')
    ax.set_yscale("log", nonposx='clip')
    plt.savefig('%s/pareto3c_%s_obj%02i_obj%02i.eps'%(plotdir,fn_suffix,objectives[i][0].id,objectives[i][1].id),format='eps',bbox_inches='tight' )
    plt.savefig('%s/pareto3c_%s_obj%02i_obj%02i.png'%(plotdir,fn_suffix,objectives[i][0].id,objectives[i][1].id),format='png',bbox_inches='tight', dpi=600 )

    if objectives[i][0].id==1: plt.xlim( bounds[0] )
    if objectives[i][0].id==2: plt.xlim( bounds[1] )
    if objectives[i][0].id==3: plt.xlim( bounds[2] )
    if objectives[i][0].id==7: plt.xlim( bounds[3] )
    if objectives[i][0].id==8: plt.xlim( bounds[4] )
    if objectives[i][0].id==9: plt.xlim( bounds[5] )

    if objectives[i][1].id==1: plt.ylim( bounds[0] )
    if objectives[i][1].id==2: plt.ylim( bounds[1] )
    if objectives[i][1].id==3: plt.ylim( bounds[2] )
    if objectives[i][1].id==7: plt.ylim( bounds[3] )
    if objectives[i][1].id==8: plt.ylim( bounds[4] )
    if objectives[i][1].id==9: plt.ylim( bounds[5] )

    plt.savefig('%s/pareto3c_%s_inset_obj%02i_obj%02i.png'%(plotdir,fn_suffix,objectives[i][0].id,objectives[i][1].id),format='png',bbox_inches='tight', dpi=600 )

    plt.close()

def plot_pareto3d(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None):

  for i in range(len(objectives)):

    print objectives[i]
    paretoRanks = start_pareto_rank_structure(opts,objectives[i])
    instx  = objectives[i][0].measurements[0].instruments[0]
    insty  = objectives[i][1].measurements[0].instruments[0]
    instz  = objectives[i][2].measurements[0].instruments[0]
    titlex = '%s %s [%s]' % (instx.title,instx.instType.abv,instx.instType.unit)
    titley = '%s %s [%s]' % (insty.title,insty.instType.abv,insty.instType.unit)
    titlez = '%s %s [%s]' % (instz.title,instz.instType.abv,instz.instType.unit)

    errs=np.zeros([0,3],dtype='float')
    rnks=[]
    optids=[]
    sampids = []
    for opt in opts:
      for sample in opt.samples:
        print sample.id, len(opt.samples)
        if sample.status()==2:
          try:
            errs0    = np.array(sample.get_errors(objectives[i])).reshape([1,3])
            if errs0[0][0]<100 and errs0[0][1]<100 and errs0[0][2]<1000:
              errs     = np.vstack([ errs, errs0 ])
              rnks    += [paretoRanks[sample.id]]
              optids  += [int(opt.id)]
              sampids += [int(sample.id)]
          except: pass

    print errs
    exMin = np.sort(errs[:,0])[0]
    eyMin = np.sort(errs[:,1])[0]
    ezMin = np.sort(errs[:,2])[0]
    exMax = np.sort(errs[:,0])[-1]
    eyMax = np.sort(errs[:,1])[-1]
    ezMax = np.sort(errs[:,2])[-1]
    dx    = 0.02*(np.log10(exMax)-np.log10(exMin))
    dy    = 0.02*(np.log10(eyMax)-np.log10(eyMin))
    dz    = 0.02*(np.log10(ezMax)-np.log10(ezMin))
    exMin = 10**(np.log10(exMin)-dx)
    eyMin = 10**(np.log10(eyMin)-dy)
    ezMin = 10**(np.log10(ezMin)-dz)
    exMax = 10**(np.log10(exMax)+dx)
    eyMax = 10**(np.log10(eyMax)+dy)
    ezMax = 10**(np.log10(ezMax)+dz)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter( errs[:,0], errs[:,1], errs[:,2], s=10, c=rnks, edgecolor='none', zorder=3 )
    ax.set_xlabel( '%s' % titlex, fontsize=22)
    ax.set_ylabel( '%s' % titley, fontsize=22)
    ax.set_xlim([exMin,exMax])
    ax.set_ylim([eyMin,eyMax])
    ax.set_zlim([ezMin,ezMax])
    an = 89.9
    th = 270.0
    iFrame = 0
    for j in range(50):
      print an, th, iFrame
      ax.view_init(an,th)
      plt.savefig('%s/pareto3d_obj%02i_obj%02i_obj%02i_iFrame%03i.eps'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto3d_obj%02i_obj%02i_obj%02i_iFrame%03i.png'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='png',bbox_inches='tight', dpi=600 )
      iFrame+=1
      an -= 60.0/50.0
      if an<80:
        th -= 20.0/40.0
      if an<60:
        ax.set_zlabel( '%s' % titlez, fontsize=22)
    for j in range(50):
      print an, th, iFrame
      ax.view_init(an,th)
      plt.savefig('%s/pareto3d_obj%02i_obj%02i_obj%02i_iFrame%03i.eps'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto3d_obj%02i_obj%02i_obj%02i_iFrame%03i.png'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='png',bbox_inches='tight', dpi=600 )
      iFrame+=1
      an -= 20.0/50.0
      th += 40.0/50.0
    plt.close()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter( np.log10(errs[:,0]), np.log10(errs[:,1]), np.log10(errs[:,2]), s=10, c=rnks, edgecolor='none', zorder=3 )
    ax.set_xlabel( '%s' % titlex, fontsize=22)
    ax.set_ylabel( '%s' % titley, fontsize=22)

    ax.set_xlim([np.log10(exMin),np.log10(exMax)])
    ax.set_ylim([np.log10(eyMin),np.log10(eyMax)])
    ax.set_zlim([np.log10(ezMin),np.log10(ezMax)])

    an = 89.9
    th = 270.0
    iFrame = 0
    for j in range(50):
      print an, th, iFrame
      ax.view_init(an,th)
      plt.savefig('%s/pareto3d_log_obj%02i_obj%02i_obj%02i_iFrame%03i.eps'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto3d_log_obj%02i_obj%02i_obj%02i_iFrame%03i.png'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='png',bbox_inches='tight', dpi=600 )
      iFrame+=1
      an -= 60.0/50.0
      if an<80:
        th -= 20.0/40.0
      if an<60:
        ax.set_zlabel( '%s' % titlez, fontsize=22)
    for j in range(50):
      print an, th, iFrame
      ax.view_init(an,th)
      plt.savefig('%s/pareto3d_log_obj%02i_obj%02i_obj%02i_iFrame%03i.eps'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto3d_log_obj%02i_obj%02i_obj%02i_iFrame%03i.png'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='png',bbox_inches='tight', dpi=600 )
      iFrame+=1
      an -= 20.0/50.0
      th += 40.0/50.0
    plt.close()

def plot_pareto3db(opts,plotdir,fn_suffix,objectives1,objectives2):

    print objectives1
#    paretoRanks = start_pareto_rank_structure(opts,objectives1)
    paretoRanks = pickle.load(open('pareto.pkl','rb'))['paretoRank']
    instx  = objectives2[0].measurements[0].instruments[0]
    insty  = objectives2[1].measurements[0].instruments[0]
    instz  = objectives2[2].measurements[0].instruments[0]
    titlex = '%s %s [%s]' % (instx.title,instx.instType.abv,instx.instType.unit)
    titley = '%s %s [%s]' % (insty.title,insty.instType.abv,insty.instType.unit)
    titlez = '%s %s [%s]' % (instz.title,instz.instType.abv,instz.instType.unit)

    errs=np.zeros([0,3],dtype='float')
    rnks=[]
    optids=[]
    sampids = []
    for opt in opts:
      for sample in opt.samples:
        print sample.id, len(opt.samples)
        if sample.status()==2:
          try:
            errs0    = np.array(sample.get_errors(objectives2)).reshape([1,3])
            if objectives2[0].id>3:
              if errs0[0][0]<1000 and errs0[0][1]<1000 and errs0[0][2]<1000:
                errs     = np.vstack([ errs, errs0 ])
                rnks    += [paretoRanks[sample.id]]
                optids  += [int(opt.id)]
                sampids += [int(sample.id)]
            else:
              if errs0[0][0]<100 and errs0[0][1]<100 and errs0[0][2]<100:
                errs     = np.vstack([ errs, errs0 ])
                rnks    += [paretoRanks[sample.id]]
                optids  += [int(opt.id)]
                sampids += [int(sample.id)]
          except: pass

    print errs
    exMin = np.sort(errs[:,0])[0]
    eyMin = np.sort(errs[:,1])[0]
    ezMin = np.sort(errs[:,2])[0]
    exMax = np.sort(errs[:,0])[-1]
    eyMax = np.sort(errs[:,1])[-1]
    ezMax = np.sort(errs[:,2])[-1]
    dx    = 0.02*(np.log10(exMax)-np.log10(exMin))
    dy    = 0.02*(np.log10(eyMax)-np.log10(eyMin))
    dz    = 0.02*(np.log10(ezMax)-np.log10(ezMin))
    exMin = 10**(np.log10(exMin)-dx)
    eyMin = 10**(np.log10(eyMin)-dy)
    ezMin = 10**(np.log10(ezMin)-dz)
    exMax = 10**(np.log10(exMax)+dx)
    eyMax = 10**(np.log10(eyMax)+dy)
    ezMax = 10**(np.log10(ezMax)+dz)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter( errs[:,0], errs[:,1], errs[:,2], s=10, c=rnks, edgecolor='none', zorder=3 )
    ax.set_xlabel( '%s' % titlex, fontsize=22)
    ax.set_ylabel( '%s' % titley, fontsize=22)
    ax.set_xlim([exMin,exMax])
    ax.set_ylim([eyMin,eyMax])
    ax.set_zlim([ezMin,ezMax])
    an = 89.9
    th = 270.0
    iFrame = 0
    for j in range(50):
      print an, th, iFrame
      ax.view_init(an,th)
      plt.savefig('%s/pareto3db_%s_obj%02i_%02i_%02i_iFrame%03i.eps'%(plotdir,fn_suffix,objectives2[0].id,objectives2[1].id,objectives2[2].id,iFrame),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto3db_%s_obj%02i_%02i_%02i_iFrame%03i.png'%(plotdir,fn_suffix,objectives2[0].id,objectives2[1].id,objectives2[2].id,iFrame),format='png',bbox_inches='tight', dpi=600 )
      iFrame+=1
      an -= 60.0/50.0
      if an<80:
        th -= 20.0/40.0
      if an<60:
        ax.set_zlabel( '%s' % titlez, fontsize=22)
    for j in range(50):
      print an, th, iFrame
      ax.view_init(an,th)
      plt.savefig('%s/pareto3db_%s_obj%02i_%02i_%02i_iFrame%03i.eps'%(plotdir,fn_suffix,objectives2[0].id,objectives2[1].id,objectives2[2].id,iFrame),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto3db_%s_obj%02i_%02i_%02i_iFrame%03i.png'%(plotdir,fn_suffix,objectives2[0].id,objectives2[1].id,objectives2[2].id,iFrame),format='png',bbox_inches='tight', dpi=600 )
      iFrame+=1
      an -= 20.0/50.0
      th += 40.0/50.0
    plt.close()

    '''fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter( np.log10(errs[:,0]), np.log10(errs[:,1]), np.log10(errs[:,2]), s=10, c=rnks, edgecolor='none', zorder=3 )
    ax.set_xlabel( '%s' % titlex, fontsize=22)
    ax.set_ylabel( '%s' % titley, fontsize=22)

    ax.set_xlim([np.log10(exMin),np.log10(exMax)])
    ax.set_ylim([np.log10(eyMin),np.log10(eyMax)])
    ax.set_zlim([np.log10(ezMin),np.log10(ezMax)])

    an = 89.9
    th = 270.0
    iFrame = 0
    for j in range(50):
      print an, th, iFrame
      ax.view_init(an,th)
      plt.savefig('%s/pareto3d_log_obj%02i_%02i_%02i_iFrame%03i.eps'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto3d_log_obj%02i_%02i_%02i_iFrame%03i.png'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='png',bbox_inches='tight', dpi=600 )
      iFrame+=1
      an -= 60.0/50.0
      if an<80:
        th -= 20.0/40.0
      if an<60:
        ax.set_zlabel( '%s' % titlez, fontsize=22)
    for j in range(50):
      print an, th, iFrame
      ax.view_init(an,th)
      plt.savefig('%s/pareto3d_log_obj%02i_%02i_%02i_iFrame%03i.eps'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto3d_log_obj%02i_%02i_%02i_iFrame%03i.png'%(plotdir,objectives[i][0].id,objectives[i][1].id,objectives[i][2].id,iFrame),format='png',bbox_inches='tight', dpi=600 )
      iFrame+=1
      an -= 20.0/50.0
      th += 40.0/50.0
    plt.close()'''

def plot_pareto3(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None):

  par_x = np.linspace(0,5,1000)
  par_y = np.linspace(0,5,1000)

  par_f1 = 4*par_x**2 + 4*par_y**2
  par_f2 = (par_x-5)**2 + (par_y-5)**2

  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  instx  = objectives[0].measurements[0].instruments[0]
  insty  = objectives[1].measurements[0].instruments[0]
  titlex = '%s %s [%s]' % (instx.title,instx.instType.abv,instx.instType.unit)
  titley = '%s %s [%s]' % (insty.title,insty.instType.abv,insty.instType.unit)

  if type(paretoRanks)==type(None):
    paretoRanks = update_pareto_rank_structure(opts,objectives[0:2])

  errs=np.zeros([0,2],dtype='float')
  rnks=[]
  for opt in opts:
    for sample in opt.samples:
      if sample.status()==2:
        errs  = np.vstack([ errs, np.array(sample.get_errors(objectives[0:2])).reshape([1,2]) ])
        rnks += [paretoRanks[sample.id]]

  ii = np.where(np.array(rnks)==1)[0]

  exMin = np.sort(errs[:,0])[0]
  eyMin = np.sort(errs[:,1])[0]
  exMax = np.sort(errs[:,0])[-3]
  eyMax = np.sort(errs[:,1])[-3]
  dx    = 0.02*(np.log10(exMax)-np.log10(exMin))
  dy    = 0.02*(np.log10(eyMax)-np.log10(eyMin))

  exMin = 10**(np.log10(exMin)-dx)
  eyMin = 10**(np.log10(eyMin)-dy)
  exMax = 10**(np.log10(exMax)+dx)
  eyMax = 10**(np.log10(eyMax)+dy)

  rank1 = errs[ii,:]
  ii = np.argsort(rank1[:,0])
  rank1 = rank1[ii]

  ig  = np.where( np.multiply( errs[:,0]<2e5, errs[:,1]<7e5 ) )[0]

  fig,ax = plt.subplots()

#  plt.plot( par_f1, par_f2, 'k--', linewidth=1, zorder=0 )

  plt.plot( rank1[:,0], rank1[:,1], linewidth=2, c=[0.7,0.7,0.7], zorder=1 )

  plt.scatter( errs[:,0], errs[:,1], s=30, c='gray', edgecolor='none', zorder=1.9 )
  sc=plt.scatter( errs[ig,0], errs[ig,1], s=30, c=np.array(rnks)[ig], edgecolor='none', zorder=2 )

  plt.xlabel( '%s' % titlex, fontsize=22)
  plt.ylabel( '%s' % titley, fontsize=22)

  plt.xlabel( 'Misfit, EW Strain [$\mu\epsilon$]', fontsize=32)
  plt.ylabel( 'Misfit, NS Strain [$\mu\epsilon$]', fontsize=32)

  plt.xlim([ exMin, exMax ])
  plt.ylim([ eyMin, eyMax ])
  plt.xlim([ 10**4.6,10**8.5 ])
  plt.ylim([ 10**4.2,10**7.8 ])
  ax.set_xscale("log", nonposx='clip')
  ax.set_yscale("log", nonposx='clip')
  if np.max(rnks)>12:
    ticks = np.linspace(1,np.max(rnks),8)
    ticks = np.round(ticks)
    cb = plt.colorbar(sc,ticks=ticks)
  else:
    cb = plt.colorbar(sc)
  cb.set_label('Pareto Rank',fontsize=32)
  plt.savefig('%s/pareto3.eps'%plotdir,format='eps',bbox_inches='tight' )
  plt.savefig('%s/pareto3.png'%plotdir,format='png',bbox_inches='tight', dpi=600 )
  plt.close()

def plot_pareto4(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None):

  par_x = np.linspace(0,5,1000)
  par_y = np.linspace(0,5,1000)

  par_f1 = 4*par_x**2 + 4*par_y**2
  par_f2 = (par_x-5)**2 + (par_y-5)**2

  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  instx  = objectives[0].measurements[0].instruments[0]
  insty  = objectives[1].measurements[0].instruments[0]
  titlex = '%s %s [%s]' % (instx.title,instx.instType.abv,instx.instType.unit)
  titley = '%s %s [%s]' % (insty.title,insty.instType.abv,insty.instType.unit)

  if type(paretoRanks)==type(None):
    paretoRanks = update_pareto_rank_structure(opts,objectives[0:2])

  errs=np.zeros([0,2],dtype='float')
  rnks=[]
  for opt in opts:
    for sample in opt.samples:
      if sample.status()==2:
        errs  = np.vstack([ errs, np.array(sample.get_errors(objectives[0:2])).reshape([1,2]) ])
        rnks += [paretoRanks[sample.id]]

  ii = np.where(np.array(rnks)==1)[0]

  exMin = np.sort(errs[:,0])[0]
  eyMin = np.sort(errs[:,1])[0]
  exMax = np.sort(errs[:,0])[-3]
  eyMax = np.sort(errs[:,1])[-3]
  dx    = 0.02*(np.log10(exMax)-np.log10(exMin))
  dy    = 0.02*(np.log10(eyMax)-np.log10(eyMin))

  exMin = 10**(np.log10(exMin)-dx)
  eyMin = 10**(np.log10(eyMin)-dy)
  exMax = 10**(np.log10(exMax)+dx)
  eyMax = 10**(np.log10(eyMax)+dy)

  rank1 = errs[ii,:]
  ii = np.argsort(rank1[:,0])
  rank1 = rank1[ii]

  ip = []
  current_rank = 1
  while True:
    if len(ip)<500:
      print list(np.where(np.array(rnks)==current_rank)[0])
      print type(list(np.where(np.array(rnks)==current_rank)[0]))
      print type(ip)
      ip.append( list(np.where(np.array(rnks)==current_rank)[0]) )
      print ip
      current_rank += 1
    else: break

  fig,ax = plt.subplots()

#  plt.plot( par_f1, par_f2, 'k--', linewidth=1, zorder=0 )

  plt.plot( rank1[:,0], rank1[:,1], linewidth=2, c=[0.7,0.7,0.7], zorder=1 )

  plt.scatter( errs[:,0], errs[:,1], s=30, c='gray', edgecolor='none', zorder=1.9 )
  sc=plt.scatter( errs[ip,0], errs[ip,1], s=30, c=np.array(rnks)[ig], edgecolor='none', zorder=2 )

  plt.xlabel( '%s' % titlex, fontsize=22)
  plt.ylabel( '%s' % titley, fontsize=22)

  plt.xlabel( 'Misfit, EW Strain [$\mu\epsilon$]', fontsize=32)
  plt.ylabel( 'Misfit, NS Strain [$\mu\epsilon$]', fontsize=32)

  plt.xlim([ exMin, exMax ])
  plt.ylim([ eyMin, eyMax ])
  plt.xlim([ 10**4.6,10**8.5 ])
  plt.ylim([ 10**4.2,10**7.8 ])
  ax.set_xscale("log", nonposx='clip')
  ax.set_yscale("log", nonposx='clip')
  if np.max(rnks)>12:
    ticks = np.linspace(1,np.max(rnks),8)
    ticks = np.round(ticks)
    cb = plt.colorbar(sc,ticks=ticks)
  else:
    cb = plt.colorbar(sc)
  cb.set_label('Pareto Rank',fontsize=32)
  plt.savefig('%s/pareto4.eps'%plotdir,format='eps',bbox_inches='tight' )
  plt.savefig('%s/pareto4.png'%plotdir,format='png',bbox_inches='tight', dpi=600 )
  plt.close()

def plot_pareto5(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None):

  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  instx  = objectives[0].measurements[0].instruments[0]
  insty  = objectives[1].measurements[0].instruments[0]
  titlex = '%s %s [%s]' % (instx.title,instx.instType.abv,instx.instType.unit)
  titley = '%s %s [%s]' % (insty.title,insty.instType.abv,insty.instType.unit)

  errs=np.zeros([0,2],dtype='float')
  for opt in opts:
    for sample in opt.samples:
      if sample.status()==2:
        errs  = np.vstack([ errs, np.array(sample.get_errors(objectives[0:2])).reshape([1,2]) ])

  exMin = np.sort(errs[:,0])[0]
  eyMin = np.sort(errs[:,1])[0]
  exMax = np.sort(errs[:,0])[-3]
  eyMax = np.sort(errs[:,1])[-3]
  dx    = 0.02*(np.log10(exMax)-np.log10(exMin))
  dy    = 0.02*(np.log10(eyMax)-np.log10(eyMin))

  exMin = 10**(np.log10(exMin)-dx)
  eyMin = 10**(np.log10(eyMin)-dy)
  exMax = 10**(np.log10(exMax)+dx)
  eyMax = 10**(np.log10(eyMax)+dy)

  fig,ax = plt.subplots()

  sc=plt.scatter( errs[:,0], errs[:,1], s=30, c='k', edgecolor='none', zorder=2 )

  plt.xlabel( '%s' % titlex, fontsize=22)
  plt.ylabel( '%s' % titley, fontsize=22)

  plt.xlabel( 'Misfit, EW Strain [$\mu\epsilon$]', fontsize=32)
  plt.ylabel( 'Misfit, NS Strain [$\mu\epsilon$]', fontsize=32)

  plt.xlim([ exMin, exMax ])
  plt.ylim([ eyMin, eyMax ])

#  plt.xlim([ 10**4.6,10**8.5 ])
#  plt.ylim([ 10**4.6,10**8.5 ])

  plt.xlim([ 10**4.2,10**8.3 ])
  plt.ylim([ 10**4.2,10**8.3 ])

  ax.set_xscale("log", nonposx='clip')
  ax.set_yscale("log", nonposx='clip')

  plt.savefig('%s/pareto5.eps'%plotdir,format='eps',bbox_inches='tight' )
  plt.savefig('%s/pareto5.png'%plotdir,format='png',bbox_inches='tight', dpi=600 )
  plt.close()

def plot_pareto_vid(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None):

  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  instx  = objectives[0].measurements[0].instruments[0]
  insty  = objectives[1].measurements[0].instruments[0]
  titlex = '%s %s [%s]' % (instx.title,instx.instType.abv,instx.instType.unit)
  titley = '%s %s [%s]' % (insty.title,insty.instType.abv,insty.instType.unit)

  if type(paretoRanks)==type(None):
    paretoRanks = update_pareto_rank_structure(opts,objectives[0:2])

  errs=np.zeros([0,2],dtype='float')
  rnks=[]
  for opt in opts:
    for sample in opt.samples:
      if sample.status()==2:
        errs  = np.vstack([ errs, np.array(sample.get_errors(objectives[0:2])).reshape([1,2]) ])
        rnks += [paretoRanks[sample.id]]

  ii = np.where(np.array(rnks)==1)[0]

  exMin = np.sort(errs[:,0])[0]
  eyMin = np.sort(errs[:,1])[0]
  exMax = np.sort(errs[:,0])[-3]
  eyMax = np.sort(errs[:,1])[-3]
  dx    = 0.02*(np.log10(exMax)-np.log10(exMin))
  dy    = 0.02*(np.log10(eyMax)-np.log10(eyMin))

  exMin = 10**(np.log10(exMin)-dx)
  eyMin = 10**(np.log10(eyMin)-dy)
  exMax = 10**(np.log10(exMax)+dx)
  eyMax = 10**(np.log10(eyMax)+dy)

  rank1 = errs[ii,:]
  ii = np.argsort(rank1[:,0])
  rank1 = rank1[ii]

  for i in range(0,ranks.shape[0],100):
    fig,ax = plt.subplots()

#    plt.plot( rank1[0:i,0], rank1[:,1], linewidth=2, c=[0.7,0.7,0.7], zorder=1 )

    sc=plt.scatter( errs[0:i,0], errs[0:i,1], s=30, c=rnks, edgecolor='none', zorder=2 )

    plt.xlabel( '%s' % titlex, fontsize=22)
    plt.ylabel( '%s' % titley, fontsize=22)

#    plt.xlabel( 'Misfit, EW Strain [$\mu\epsilon$]', fontsize=32)
#    plt.ylabel( 'Misfit, NS Strain [$\mu\epsilon$]', fontsize=32)

    plt.xlim([ exMin, exMax ])
    plt.ylim([ eyMin, eyMax ])

    ax.set_xscale("log", nonposx='clip')
    ax.set_yscale("log", nonposx='clip')
    if np.max(rnks)>12:
      ticks = np.linspace(1,np.max(rnks),8)
      ticks = np.round(ticks)
      cb = plt.colorbar(sc,ticks=ticks)
    else:
      cb = plt.colorbar(sc)
    cb.set_label('Pareto Rank',fontsize=32)
    plt.savefig('%s/pareto_vid_%03i.png'%plotdir,format='png',bbox_inches='tight', dpi=300 )
    plt.close()

def plot_pareto_hist(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None,bounds=None,truePars=None):
  if type(objectives)==type(None):
    objectives=[]
    for opt in opts:
      objectives += opt.objectives
    objectives = list(set(objectives))

  parameters = opts[0].parameters

  count=0
  ests    = []
  estsAll = []
  errs    = []
  erns    = []
  erns1   = []
  erns2   = []
  rnks    = []
  inBds   = []
  j  = 0
  jj = []
  kk = []
  kk1 = []
  kk2 = []
  for opt in opts:
    for sample in opt.samples:
      #if sample.id>1000: break
      if sample.status()==2:
        if paretoRanks[int(sample.id)]<50:

          exx = sample.get_predictions(objectives[0])[0].fetch_misfit()
          eyy = sample.get_predictions(objectives[1])[0].fetch_misfit()
          ezz = sample.get_predictions(objectives[2])[0].fetch_misfit()
          #pf1 = sample.get_predictions(objectives[6])[0].fetch_misfit()
          #pf2 = sample.get_predictions(objectives[7])[0].fetch_misfit()
          #pf3 = sample.get_predictions(objectives[8])[0].fetch_misfit()
          #if exx<12 and eyy<12 and ezz<12:
          #  if pf1<50 and pf2<110 and pf3<80:
          #if exx<10 and eyy<15 and ezz<15:
          #if pf1<25 and pf2<30 and pf3<35:
          estsAll     += [0]
          estsAll[-1]  = [sample.get_estimates(param)[0].value for param in parameters]
          #if True:

          # 137
          #k1 = sample.get_estimates(opts[0].parameters[0])[0].value
          #k2 = sample.get_estimates(opts[0].parameters[7])[0].value
          #k3 = sample.get_estimates(opts[0].parameters[5])[0].value

          # 144
          #k1 = sample.get_estimates(opts[0].parameters[4])[0].value
          #k2 = sample.get_estimates(opts[0].parameters[11])[0].value
          #k3 = sample.get_estimates(opts[0].parameters[0])[0].value

          # 145
          #k1 = sample.get_estimates(opts[0].parameters[4])[0].value
          #k2 = sample.get_estimates(opts[0].parameters[13])[0].value
          #k3 = sample.get_estimates(opts[0].parameters[0])[0].value

          # 157
          #k1 = sample.get_estimates(opts[0].parameters[8])[0].value
          #k2 = sample.get_estimates(opts[0].parameters[10])[0].value
          #k3 = sample.get_estimates(opts[0].parameters[7])[0].value

          # 169
          k1 = sample.get_estimates(opts[0].parameters[6])[0].value
          k2 = sample.get_estimates(opts[0].parameters[7])[0].value
          k3 = sample.get_estimates(opts[0].parameters[3])[0].value

          ests     += [0]
          ests[-1]  = [sample.get_estimates(param)[0].value for param in parameters]
          errs     += [0]
          errs[-1]  = sample.get_errors(objectives)
          ern  = 0
          ern1 = 0
          ern2 = 0
          ern += errs[-1][0]/float(objectives[0].measurements[0].sigsq)**0.5
          ern += errs[-1][1]/float(objectives[1].measurements[0].sigsq)**0.5
          ern += errs[-1][2]/float(objectives[2].measurements[0].sigsq)**0.5
          #ern += errs[-1][6]/float(objectives[6].measurements[0].sigsq)**0.5
          #ern += errs[-1][7]/float(objectives[7].measurements[0].sigsq)**0.5
          #ern += errs[-1][8]/float(objectives[8].measurements[0].sigsq)**0.5

          ern1 += errs[-1][0]/float(objectives[0].measurements[0].sigsq)**0.5
          ern1 += errs[-1][1]/float(objectives[1].measurements[0].sigsq)**0.5
          ern1 += errs[-1][2]/float(objectives[2].measurements[0].sigsq)**0.5
          #ern2 += errs[-1][6]/float(objectives[6].measurements[0].sigsq)**0.5
          #ern2 += errs[-1][7]/float(objectives[7].measurements[0].sigsq)**0.5
          #ern2 += errs[-1][8]/float(objectives[8].measurements[0].sigsq)**0.5
          erns  += [ern]
          erns1 += [ern1]
          #erns2 += [ern2]
          #print errs[-1][0],errs[-1][1],errs[-1][2],errs[-1][6],errs[-1][7],errs[-1][8]
          #print objectives[0].measurements[0].sigsq**0.5,objectives[1].measurements[0].sigsq**0.5,objectives[2].measurements[0].sigsq**0.5,objectives[6].measurements[0].sigsq**0.5,objectives[7].measurements[0].sigsq**0.5,objectives[8].measurements[0].sigsq**0.5
          #print sample.id, np.sum([len(opt.samples) for opt in opts]), ern

          rnks += [paretoRanks[int(sample.id)]]
          count    += 1

          print k1, k2, k3
          print sample.id, np.sum([len(opt.samples) for opt in opts]), ern

          if True:
            kk += [j]

          #if exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] and \
          #   pf1<bounds[3] and pf2<bounds[4] and pf3<bounds[5]:
          #     jj+= [j]
          #     if k1>k2 and k2>k3 and k3<-16:
          #       kk += [j]

          #if exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] and \
          #   k1>k2 and k2>k3 and k3<-16:
          #     kk1 += [j]

          #if pf1<bounds[3] and pf2<bounds[4] and pf3<bounds[5] and \
          #   k1>k2 and k2>k3 and k3<-16:
          #     kk2 += [j]

          j+=1

  pickle.dump({'count':count,'ests':ests,'estsAll':estsAll,'errs':errs,'erns':erns,'erns1':erns1,'erns2':erns2,'rnks':rnks,'inBds':inBds,'j':j,'jj':jj,'kk':kk,'kk1':kk1,'kk2':kk2},open('plot_data.pkl','wb'))
  #exit()

  temp=pickle.load(open('plot_data.pkl','rb'))

  count   = temp['count']
  ests    = temp['ests']
  estsAll = temp['estsAll']
  errs    = temp['errs']
  erns    = temp['erns']
  erns1   = temp['erns1']
  erns2   = temp['erns2']
  rnks    = temp['rnks']
  inBds   = temp['inBds']
  j       = temp['j']
  jj      = temp['jj']
  kk      = temp['kk']
  kk1     = temp['kk1']
  kk2     = temp['kk2']

  estsAll = np.array(estsAll)
  ests = np.array(ests)
  errs = np.array(errs)
  erns = np.array(erns)
  erns1 = np.array(erns1)
  erns2 = np.array(erns2)

  print 'ests', ests.shape
  print 'all', estsAll.shape
  print len(jj), len(kk)
  #exit()

  for i in range(len(parameters)):

    print parameters[i].structure.domain.id, parameters[i].property.id
    print parameters[i].structure.domain.title, parameters[i].property.title

    vmin = parameters[i].get_pxd().priorModel.min
    vmax = parameters[i].get_pxd().priorModel.max

    plt.figure()
    #w = np.ones_like(ests[kk1,i])/float(len(ests[kk1,i]))
    #plt.hist(ests[kk1,i], weights=w, alpha=1.0,bins=np.arange(vmin,vmax,(vmax-vmin)/30.0), color='red', label='S', zorder=0)
    w = np.ones_like(ests[kk,i])/float(len(ests[kk,i]))
    plt.hist(ests[kk,i],  weights=w, alpha=0.4,bins=np.arange(vmin,vmax,(vmax-vmin)/30.0), color='blue', label='P+S', zorder=1)
    #w = np.ones_like(ests[kk1,i])/float(len(ests[kk1,i]))
    #plt.hist(ests[kk1,i],label='Strain', weights=w, alpha=0.4)
    ylim=plt.gca().get_ylim()
    if not type(truePars)==type(None):
      plt.plot([truePars[i],truePars[i]],[ylim[0],ylim[1]],'--k')
    plt.xlabel('%s %s'% (parameters[i].structure.domain.title,parameters[i].property.title),fontsize=36)
    plt.xlim([vmin,vmax])
    for tick in plt.gca().xaxis.get_major_ticks(): tick.label.set_fontsize(18)
    for tick in plt.gca().yaxis.get_major_ticks(): tick.label.set_fontsize(18)
    plt.legend()
    plt.savefig('%s/pareto_%s_hist_par%02i.eps'%(plotdir,fn_suffix,parameters[i].id),format='eps',bbox_inches='tight' )
    plt.savefig('%s/pareto_%s_hist_par%02i.png'%(plotdir,fn_suffix,parameters[i].id),format='png',bbox_inches='tight', dpi=100 )
    plt.close()

    ii = np.array(jj)[np.argsort(erns[jj])[::-1]]
    fig,ax=plt.subplots()
    plt.scatter(ests[:,i],np.array(erns),s=15,c='r',edgecolor='none',label='P+S',zorder=1)
    #plt.scatter(ests[:,i],np.log10(np.array(erns1)),s=15,c='g',edgecolor='none')
    #plt.scatter(ests[:,i],np.array(erns2),s=15,c='b',edgecolor='none',alpha=1.0,label='P',zorder=0)
    plt.xlabel('%s %s'% (parameters[i].structure.domain.title,parameters[i].property.title),fontsize=36)
    plt.ylabel('Weighted Error',fontsize=36)
    plt.xlim([vmin,vmax])
    plt.ylim([10,300])
    plt.yticks([10,100],['10','100'])
    ax.set_yscale("log", nonposx='clip')
    plt.legend()
    #plt.savefig('%s/pareto_%s_hist2_par%02i.eps'%(plotdir,fn_suffix,parameters[i].id),format='eps',bbox_inches='tight' )
    plt.savefig('%s/pareto_%s_hist2_par%02i.png'%(plotdir,fn_suffix,parameters[i].id),format='png',bbox_inches='tight', dpi=100 )
    plt.close()

  #exit()
  for i in range(len(parameters)):
    for j in range(len(parameters)):
      if i==j: continue
      print i,j

      print parameters[i].structure.domain.id,    parameters[i].property.id
      print parameters[i].structure.domain.title, parameters[i].property.title
      print parameters[j].structure.domain.id,    parameters[j].property.id
      print parameters[j].structure.domain.title, parameters[j].property.title

      vmini = parameters[i].get_pxd().priorModel.min
      vmaxi = parameters[i].get_pxd().priorModel.max
      vminj = parameters[j].get_pxd().priorModel.min
      vmaxj = parameters[j].get_pxd().priorModel.max

      norm = matplotlib.colors.LogNorm(vmin=np.min(erns),vmax=300)

      ii = np.argsort(erns)[::-1]
      ii = np.array(jj)[np.argsort(erns[jj])[::-1]]
      ii = np.argsort(erns)[::-1]
      plt.figure()
      #plt.scatter(estsAll[:,i],estsAll[:,j],s=16,c=[0.75,0.75,0.75],edgecolor='none')
      #sc=plt.scatter(ests[:,i],ests[:,j],s=30,c=[0.6,0.6,0.6],edgecolor='none')
      #sc=plt.scatter(ests[:,i],ests[:,j],s=15,c=np.array(erns)[:],edgecolor='none',vmin=6,vmax=40,alpha=0.4)
      sc=plt.scatter(ests[ii,i],ests[ii,j],s=15,c=np.array(erns)[ii],edgecolor='none',vmin=np.min(erns),vmax=300,norm=norm)
      #sc=plt.scatter(ests[ii,i],ests[ii,j],s=15,c=np.array(erns)[ii],edgecolor='none',vmin=6,vmax=400)
      #if not type(truePars)==type(None):
      #  plt.scatter(truePars[i],truePars[j],s=300,c='black',marker='*',edgecolor='none')
      #  plt.scatter(truePars[i],truePars[j],s=80,c='white',marker='*',edgecolor='none')
      plt.xlim([vmini,vmaxi])
      plt.ylim([vminj,vmaxj])
      plt.tick_params(axis='both', which='major', labelsize=18)
      plt.savefig('%s/pareto_%s_scatter_par%02i_par%02i.eps'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto_%s_scatter_par%02i_par%02i.png'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='png',bbox_inches='tight', dpi=100 )
      plt.xlabel('%s %s'% (parameters[i].structure.domain.title,parameters[i].property.title),fontsize=22)
      plt.ylabel('%s %s'% (parameters[j].structure.domain.title,parameters[j].property.title),fontsize=22)
      cb=plt.colorbar(sc,ticks=[50,75,100,150,200,250,300])
      cb.set_label('Weighted Error',fontsize=23)
      cb.ax.set_yticklabels(['50','75','100','150','200','250','300'])
      plt.savefig('%s/pareto_%s_scatter_par%02i_par%02i_labels.eps'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto_%s_scatter_par%02i_par%02i_labels.png'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='png',bbox_inches='tight', dpi=100 )
      plt.close()

      norm = matplotlib.colors.LogNorm(vmin=np.min(erns1),vmax=300)

      ii = np.argsort(erns1)[::-1]
      ii = np.array(jj)[np.argsort(erns1[jj])[::-1]]
      ii = np.argsort(erns1)[::-1]
      plt.figure()
      #plt.scatter(estsAll[:,i],estsAll[:,j],s=16,c=[0.75,0.75,0.75],edgecolor='none')
      #sc=plt.scatter(ests[:,i],ests[:,j],s=15,c=np.array(erns1)[:],edgecolor='none',vmin=6,vmax=40,alpha=0.4)
      sc=plt.scatter(ests[ii,i],ests[ii,j],s=15,c=np.array(erns1)[ii],edgecolor='none',vmin=np.min(erns1),vmax=300,norm=norm)
      #sc=plt.scatter(ests[ii,i],ests[ii,j],s=15,c=np.array(erns)[ii],edgecolor='none',vmin=6,vmax=400)
      if not type(truePars)==type(None):
        plt.scatter(truePars[i],truePars[j],s=300,c='black',marker='*',edgecolor='none')
        plt.scatter(truePars[i],truePars[j],s=80,c='white',marker='*',edgecolor='none')
      plt.xlim([vmini,vmaxi])
      plt.ylim([vminj,vmaxj])
      plt.tick_params(axis='both', which='major', labelsize=18)
      plt.savefig('%s/pareto2_%s_scatter_par%02i_par%02i.eps'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto2_%s_scatter_par%02i_par%02i.png'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='png',bbox_inches='tight', dpi=100 )
      plt.xlabel('%s %s'% (parameters[i].structure.domain.title,parameters[i].property.title),fontsize=22)
      plt.ylabel('%s %s'% (parameters[j].structure.domain.title,parameters[j].property.title),fontsize=22)
      cb=plt.colorbar(sc,ticks=[25,50,75,100,150,200,250,300])
      cb.set_label('Weighted Error',fontsize=23)
      cb.ax.set_yticklabels(['25','50','75','100','150','200','250','300'])
      plt.savefig('%s/pareto2_%s_scatter_par%02i_par%02i_labels.eps'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto2_%s_scatter_par%02i_par%02i_labels.png'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='png',bbox_inches='tight', dpi=100 )
      plt.close()

      ii = np.argsort(rnks)[::-1]
      plt.figure()
      sc=plt.scatter(ests[ii,i],ests[ii,j],s=15,c=np.array(rnks)[ii],edgecolor='none')
      #if not type(truePars)==type(None):
      #  plt.scatter(truePars[i],truePars[j],s=300,c='black',marker='*',edgecolor='none')
      #  plt.scatter(truePars[i],truePars[j],s=80,c='white',marker='*',edgecolor='none')
      plt.xlim([vmini,vmaxi])
      plt.ylim([vminj,vmaxj])
      plt.tick_params(axis='both', which='major', labelsize=18)
      plt.savefig('%s/pareto3_%s_scatter_par%02i_par%02i.eps'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto3_%s_scatter_par%02i_par%02i.png'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='png',bbox_inches='tight', dpi=100 )
      plt.xlabel('%s %s'% (parameters[i].structure.domain.title,parameters[i].property.title),fontsize=22)
      plt.ylabel('%s %s'% (parameters[j].structure.domain.title,parameters[j].property.title),fontsize=22)
      cb=plt.colorbar(sc)
      cb.set_label('Pareto Rank',fontsize=23)
      plt.savefig('%s/pareto3_%s_scatter_par%02i_par%02i_labels.eps'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='eps',bbox_inches='tight' )
      plt.savefig('%s/pareto3_%s_scatter_par%02i_par%02i_labels.png'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id),format='png',bbox_inches='tight', dpi=100 )
      plt.close()

      '''for k in range(len(objectives)):

        #norm = mpl.colors.Normalize( vmin=np.min(errs[:,k]), vmax=np.max(errs[:,k]) )
        #cmap = cm.ScalarMappable( norm=norm, cmap=mpl.cm.jet )

        plt.figure()
        sc=plt.scatter( estsAll[:,i], estsAll[:,j], s=10, c=errsAll[:,k], edgecolor='none' )
        cb=plt.colorbar(cmap)
        plt.xlim([vmini,vmaxi])
        plt.ylim([vminj,vmaxj])
        plt.savefig('%s/pareto_%s_scatter_par%02i_par%02i_obj%02i.eps'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id,objectives[k].id),format='eps',bbox_inches='tight' )
        plt.savefig('%s/pareto_%s_scatter_par%02i_par%02i_obj%02i.png'%(plotdir,fn_suffix,parameters[i].id,parameters[j].id,objectives[k].id),format='png',bbox_inches='tight', dpi=600 )
        plt.close()'''

  print 'ests', ests.shape
  print 'all', estsAll.shape

def plot_pareto_pilotPoints(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None,bounds=None):

  xyz  = pickle.load( open('./mesh.pkl','rb') )['hex_xyzs']
  ii = np.where(np.multiply(xyz[:,2]>-5,xyz[:,2]<0))[0]
  xy = xyz[ii,0:2]
  vor = scipy.spatial.Voronoi(xy)

  elW = np.zeros(xy.shape[0],dtype='float')
  samples = opts[0].get_complete_samples()
  for sample in samples:

    '''cx=sample.get_estimates(opts[0].parameters[8])[0].value
    cy=sample.get_estimates(opts[0].parameters[9])[0].value
    el=sample.get_estimates(opts[0].parameters[10])[0].value
    ew=sample.get_estimates(opts[0].parameters[11])[0].value
    ea=sample.get_estimates(opts[0].parameters[12])[0].value

    #print cx,cy,el,ew,ea
    #print opts[0].parameters[8].get_pxd().property.title
    #print opts[0].parameters[9].get_pxd().property.title
    #print opts[0].parameters[10].get_pxd().property.title
    #print opts[0].parameters[11].get_pxd().property.title
    #print opts[0].parameters[12].get_pxd().property.title

    z=[]
    for i in range(xy.shape[0]):
      wx = xy[i,0]
      wy = xy[i,1]
      cos_angle = np.cos(np.radians(180.-ea))
      sin_angle = np.sin(np.radians(180.-ea))
      xc0 = wx - cx
      yc0 = wy - cy
      xct = xc0 * cos_angle - yc0 * sin_angle
      yct = xc0 * sin_angle + yc0 * cos_angle
      rad_cc = (xct**2/(el/2.)**2) + (yct**2/(ew/2.)**2)
      if rad_cc<1: z+=[1]
      else:        z+=[0]
    z  = np.array(z)
    misc=np.where(z==1)[0]'''
    #print misc
    #exit()

    rank = paretoRanks[sample.id]

    exx = sample.get_predictions(objectives[0])[0].fetch_misfit()
    eyy = sample.get_predictions(objectives[1])[0].fetch_misfit()
    ezz = sample.get_predictions(objectives[2])[0].fetch_misfit()
    pf1 = sample.get_predictions(objectives[6])[0].fetch_misfit()
    pf2 = sample.get_predictions(objectives[7])[0].fetch_misfit()
    pf3 = sample.get_predictions(objectives[8])[0].fetch_misfit()

    '''# 137
    k1 = sample.get_estimates(opts[0].parameters[0])[0].value
    k2 = sample.get_estimates(opts[0].parameters[7])[0].value
    k3 = sample.get_estimates(opts[0].parameters[5])[0].value

    # 144
    k1 = sample.get_estimates(opts[0].parameters[4])[0].value
    k2 = sample.get_estimates(opts[0].parameters[11])[0].value
    k3 = sample.get_estimates(opts[0].parameters[0])[0].value

    # 145
    k1 = sample.get_estimates(opts[0].parameters[4])[0].value
    k2 = sample.get_estimates(opts[0].parameters[13])[0].value
    k3 = sample.get_estimates(opts[0].parameters[0])[0].value'''

    # 157
    k1 = sample.get_estimates(opts[0].parameters[8])[0].value
    k2 = sample.get_estimates(opts[0].parameters[10])[0].value
    k3 = sample.get_estimates(opts[0].parameters[7])[0].value

    if k1>k2 and k2>k3 \
        and exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] \
        and pf1<bounds[3] and pf2<bounds[4] and pf3<bounds[5]:

      for i in sample.misc:
      #for i in misc:
        errs    = sample.get_errors(objectives)
        ern     = 0
        ern    += errs[0]/float(objectives[0].measurements[0].sigsq)**0.5
        ern    += errs[1]/float(objectives[1].measurements[0].sigsq)**0.5
        ern    += errs[2]/float(objectives[2].measurements[0].sigsq)**0.5
        ern    += errs[3]/float(objectives[6].measurements[0].sigsq)**0.5
        ern    += errs[4]/float(objectives[7].measurements[0].sigsq)**0.5
        ern    += errs[5]/float(objectives[8].measurements[0].sigsq)**0.5
        elW[i] += 6.0/ern

  vmin = np.min(elW)
  vmax = np.max(elW)
  norm = mpl.colors.Normalize( vmin=vmin, vmax=vmax )
  cmap = cm.ScalarMappable( norm=norm, cmap=mpl.cm.jet )

  plt.figure()
  v=np.linspace(vmin,vmax,100)
  sc=plt.scatter(v,v,s=10,c=v,cmap=mpl.cm.jet)
  plt.close()

  plt.figure()
  for i in range(xy.shape[0]):
    ir = vor.point_region[i]
    iv = vor.regions[ir]
    v  = vor.vertices[iv]
    if -1 in iv: continue
    plt.fill(v[:,0],v[:,1],facecolor=cmap.to_rgba(elW[i]),zorder=0,edgecolor='k',linewidth=0.3)
    plt.scatter(xy[i,0],xy[i,1],s=2,c='k',edgecolor='none',zorder=1)
  cb=plt.colorbar(sc)
  cb.set_label('Rank Weight',fontsize=18)

  xy = np.array([ [ +239.8,  -75.3, +515.0 ],
                  [ +206.8,  -60.5, +495.0 ],
                  [ +374.6, -199.1,   -3.0 ],
                  [ -375.9,   -5.4,   -3.0 ],
                  [ -185.0,  +28.7,   -3.0 ],
                  [ -245.0, -111.7,   -3.0 ],
                  [   +0.0,   -0.0,   -3.0 ] ], dtype='float')

  plt.scatter( xy[0,0], xy[0,1], s=20, c='white', zorder=1 )
  plt.scatter( xy[3,0], xy[3,1], s=20, c='white', zorder=1 )
  plt.scatter( xy[4,0], xy[4,1], s=20, c='white', zorder=1 )
  plt.scatter( xy[5,0], xy[5,1], s=20, c='white', zorder=1 )
  plt.scatter( xy[6,0], xy[6,1], s=20, c='white', zorder=1 )

  plt.scatter( xy[0,0], xy[0,1], s=18, c='black', zorder=1 )
  plt.scatter( xy[3,0], xy[3,1], s=18, c='black', zorder=1 )
  plt.scatter( xy[4,0], xy[4,1], s=18, c='black', zorder=1 )
  plt.scatter( xy[5,0], xy[5,1], s=18, c='black', zorder=1 )
  plt.scatter( xy[6,0], xy[6,1], s=18, c='black', zorder=1 )

  txt1=plt.text( xy[0,0]+150, xy[0,1]+30, fontsize=14, color='black', va='center', ha='center', s='AVN2')
  txt2=plt.text( xy[3,0]+60,  xy[3,1]+30, fontsize=14, color='black', va='center', ha='center', s='27')
  txt3=plt.text( xy[4,0]+60,  xy[4,1]+30, fontsize=14, color='black', va='center', ha='center', s='29')
  txt4=plt.text( xy[5,0]+60,  xy[5,1]+30, fontsize=14, color='black', va='center', ha='center', s='60')
  txt5=plt.text( xy[6,0]+60,  xy[6,1]+30, fontsize=14, color='black', va='center', ha='center', s='9A')

  txt1.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])
  txt2.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])
  txt3.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])
  txt4.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])
  txt5.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])

  plt.xlim([-1000,+1000])
  plt.ylim([-1000,+1000])
  plt.savefig('%s/pareto_%s_pilotPoints.eps'%(plotdir,fn_suffix),format='eps',bbox_inches='tight' )
  plt.savefig('%s/pareto_%s_pilotPoints.png'%(plotdir,fn_suffix),format='png',bbox_inches='tight', dpi=600 )
  plt.close()

def plot_pareto_pilotPoints2(opts,plotdir,fn_suffix,objectives=None,paretoRanks=None,bounds=None):

  xyz  = pickle.load( open('./mesh.pkl','rb') )['hex_xyzs']
  ii = np.where(np.multiply(xyz[:,2]>-5,xyz[:,2]<0))[0]
  xy = xyz[ii,0:2]
  vor = scipy.spatial.Voronoi(xy)

  vmin = 0
  vmax = 1
  norm = mpl.colors.Normalize( vmin=vmin, vmax=vmax )
  cmap = cm.ScalarMappable( norm=norm, cmap=mpl.cm.jet )

  plt.figure()
  v=np.linspace(vmin,vmax,100)
  sc=plt.scatter(v,v,s=10,c=v,cmap=mpl.cm.jet)
  plt.close()

  meas = objectives[0].measurements[0]
  pred = opts[0].samples[0].get_predictions(objectives[0])[0]
  indVars,data = meas.detrend(pred)

  ests    = []
  errs    = []
  erns    = []
  rnks    = []
  preds   = np.zeros([0,6,len(indVars)],dtype='float')

  for sample in opts[0].get_complete_samples():
    if sample.status()==2:
      if paretoRanks[sample.id]==1:
        #if sample.id>500: break

        exx = sample.get_predictions(objectives[0])[0].fetch_misfit()
        eyy = sample.get_predictions(objectives[1])[0].fetch_misfit()
        ezz = sample.get_predictions(objectives[2])[0].fetch_misfit()
        pf1 = sample.get_predictions(objectives[6])[0].fetch_misfit()
        pf2 = sample.get_predictions(objectives[7])[0].fetch_misfit()
        pf3 = sample.get_predictions(objectives[8])[0].fetch_misfit()

        k1 = sample.get_estimates(opts[0].parameters[0])[0].value
        k2 = sample.get_estimates(opts[0].parameters[7])[0].value
        k3 = sample.get_estimates(opts[0].parameters[5])[0].value

        k1 = sample.get_estimates(opts[0].parameters[8])[0].value
        k2 = sample.get_estimates(opts[0].parameters[10])[0].value
        k3 = sample.get_estimates(opts[0].parameters[7])[0].value

        if k1>k2 and k2>k3 and \
          exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2] and \
          pf1<bounds[3] and pf2<bounds[4] and pf3<bounds[5]:

            preds = np.append( preds, np.zeros([1,6,len(indVars)],dtype='float'), axis=0 )
            iobjs = [0,1,2,6,7,8]
            for i in range(len(iobjs)):
              obj  = objectives[iobjs[i]]
              meas = obj.measurements[0]
              pred = sample.get_predictions(obj)[0]
              indVars,data = meas.detrend(pred)
              preds[-1,i,:] = data

            ests     += [0]
            ests[-1]  = [sample.get_estimates(param)[0].value for param in opts[0].parameters]
            errs     += [0]
            errs[-1]  = sample.get_errors(objectives)
            ern       = 0
            ern      += errs[-1][0]/float(objectives[0].measurements[0].sigsq)**0.5
            ern      += errs[-1][1]/float(objectives[1].measurements[0].sigsq)**0.5
            ern      += errs[-1][2]/float(objectives[2].measurements[0].sigsq)**0.5
            ern      += errs[-1][6]/float(objectives[6].measurements[0].sigsq)**0.5
            ern      += errs[-1][7]/float(objectives[7].measurements[0].sigsq)**0.5
            ern      += errs[-1][8]/float(objectives[8].measurements[0].sigsq)**0.5
            erns     += [ern]
            rnks     += [paretoRanks[int(sample.id)]]

  ests = np.array(ests)
  errs = np.array(errs)
  erns = np.array(erns)

  for sample in opts[0].get_complete_samples():
    if sample.status()==2:
      if paretoRanks[sample.id]==1:

        exx = sample.get_predictions(objectives[0])[0].fetch_misfit()
        eyy = sample.get_predictions(objectives[1])[0].fetch_misfit()
        ezz = sample.get_predictions(objectives[2])[0].fetch_misfit()
        pf1 = sample.get_predictions(objectives[6])[0].fetch_misfit()
        pf2 = sample.get_predictions(objectives[7])[0].fetch_misfit()
        pf3 = sample.get_predictions(objectives[8])[0].fetch_misfit()

        if exx<bounds[0] and eyy<bounds[1] and ezz<bounds[2]:
          if pf1<bounds[3] and pf2<bounds[4] and pf3<bounds[5]:

            print sample.id

            plt.figure(figsize=(24,12))

            ax1 = plt.subplot2grid( (6,12), (0,0), colspan=5, rowspan=4 )
            for i in range(xy.shape[0]):
              ir = vor.point_region[i]
              iv = vor.regions[ir]
              v  = vor.vertices[iv]
              if -1 in iv: continue
              if i in sample.misc:
                ax1.fill(v[:,0],v[:,1],facecolor=cmap.to_rgba(1),zorder=0,edgecolor='k',linewidth=0.1)
              else:
                ax1.fill(v[:,0],v[:,1],facecolor=cmap.to_rgba(0),zorder=0,edgecolor='k',linewidth=0.1)
              #ax1.scatter(xy[i,0],xy[i,1],s=2,c='k',edgecolor='none',zorder=1)
            #cb=plt.colorbar(sc)
            ax1.set_xlabel('Easting [m]', fontsize=18)
            ax1.set_ylabel('Northing [m]', fontsize=18)
            ax1.set_xlim([-1000,+1000])
            ax1.set_ylim([-1000,+1000])
            ax1.set_aspect('equal')

            ax1.text(1400,+775,'Permeability',  rotation=90, ha='center', va='center', fontsize=16 )
            ax1.text(1400,+265,'Bulk Modulus',  rotation=90, ha='center', va='center', fontsize=16 )
            ax1.text(1400,-290,'Porosity',      rotation=90, ha='center', va='center', fontsize=16 )
            ax1.text(1400,-780,'Poisson Ratio', rotation=90, ha='center', va='center', fontsize=16 )

            ax1.text(2100,+1050,'Formation', ha='center', va='center', fontsize=16 )
            ax1.text(3150,+1050,'Lens',      ha='center', va='center', fontsize=16 )
            ax1.text(4200,+1050,'Confining', ha='center', va='center', fontsize=16 )

            ax2 = plt.subplot2grid( (6,12), (0,5), colspan=2 )
            ii = np.where([(param.property.id==1 and param.structure.domain.id==1) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)
            ax2.set_xticks([-16,-15,-14,-13,-12])
            ax2 = plt.subplot2grid( (6,12), (1,5), colspan=2 )
            ii = np.where([(param.property.id==2 and param.structure.domain.id==1) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)
            ax2 = plt.subplot2grid( (6,12), (2,5), colspan=2 )
            ii = np.where([(param.property.id==3 and param.structure.domain.id==1) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)
            ax2 = plt.subplot2grid( (6,12), (3,5), colspan=2 )
            ii = np.where([(param.property.id==4 and param.structure.domain.id==1) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)

            ax2 = plt.subplot2grid( (6,12), (0,7), colspan=2 )
            ii = np.where([(param.property.id==1 and param.structure.domain.id==2) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)
            ax2.set_xticks([-14,-13,-12,-11,-10])
            ax2 = plt.subplot2grid( (6,12), (1,7), colspan=2 )
            ii = np.where([(param.property.id==2 and param.structure.domain.id==2) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)
            ax2 = plt.subplot2grid( (6,12), (2,7), colspan=2 )
            ii = np.where([(param.property.id==3 and param.structure.domain.id==2) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)
            ax2 = plt.subplot2grid( (6,12), (3,7), colspan=2 )
            ii = np.where([(param.property.id==4 and param.structure.domain.id==2) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)

            ax2 = plt.subplot2grid( (6,12), (0,9), colspan=2 )
            ii = np.where([(param.property.id==1 and param.structure.domain.id==3) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)
            ax2 = plt.subplot2grid( (6,12), (1,9), colspan=2 )
            ii = np.where([(param.property.id==2 and param.structure.domain.id==3) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)
            ax2 = plt.subplot2grid( (6,12), (2,9), colspan=2 )
            ii = np.where([(param.property.id==3 and param.structure.domain.id==3) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)
            ax2 = plt.subplot2grid( (6,12), (3,9), colspan=2 )
            ii = np.where([(param.property.id==4 and param.structure.domain.id==3) for param in opts[0].parameters])[0][0]
            ax2.hist( ests[:,ii] )
            ax2.set_xlim([opts[0].parameters[ii].get_pxd().priorModel.min,opts[0].parameters[ii].get_pxd().priorModel.max])
            val = sample.get_estimates(opts[0].parameters[ii])[0].value
            ax2.plot( [val,val], ax2.get_ylim(), 'r--', linewidth=2.0 )
            ax2.get_yaxis().set_visible(False)

            xx = np.append(indVars,indVars[::-1])

            ax2 = plt.subplot2grid( (6,12), (4,0), colspan=2, rowspan=2 )
            yy = np.append(np.max(preds[:,0,:],axis=0),np.min(preds[:,0,:],axis=0)[::-1])
            ax2.fill( xx,yy, facecolor=[0.6,0.6,0.6], edgecolor='none', zorder=0 )
            obj = objectives[0]
            pred = sample.get_predictions(obj)[0]
            meas = obj.measurements[0]
            indVars,data = meas.detrend(pred)
            plt.plot( indVars, data, c='k', zorder=1 )
            ax2.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=2 )
            ax2.set_xlim([ np.min(meas.indVars_actual),np.max(meas.indVars_actual) ])

            ax2 = plt.subplot2grid( (6,12), (4,2), colspan=2, rowspan=2 )
            yy = np.append(np.max(preds[:,1,:],axis=0),np.min(preds[:,1,:],axis=0)[::-1])
            ax2.fill( xx,yy, facecolor=[0.6,0.6,0.6], edgecolor='none', zorder=0 )
            obj = objectives[1]
            pred = sample.get_predictions(obj)[0]
            meas = obj.measurements[0]
            indVars,data = meas.detrend(pred)
            plt.plot( indVars, data, c='k', zorder=1 )
            ax2.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=2 )
            ax2.set_xlim([ np.min(meas.indVars_actual),np.max(meas.indVars_actual) ])

            ax2 = plt.subplot2grid( (6,12), (4,4), colspan=2, rowspan=2 )
            yy = np.append(np.max(preds[:,2,:],axis=0),np.min(preds[:,2,:],axis=0)[::-1])
            ax2.fill( xx,yy, facecolor=[0.6,0.6,0.6], edgecolor='none', zorder=0 )
            obj = objectives[2]
            pred = sample.get_predictions(obj)[0]
            meas = obj.measurements[0]
            indVars,data = meas.detrend(pred)
            plt.plot( indVars, data, c='k', zorder=1 )
            ax2.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=2 )
            ax2.set_xlim([ np.min(meas.indVars_actual),np.max(meas.indVars_actual) ])

            ax2 = plt.subplot2grid( (6,12), (4,6), colspan=2, rowspan=2 )
            yy = np.append(np.max(preds[:,3,:],axis=0),np.min(preds[:,3,:],axis=0)[::-1])
            ax2.fill( xx,yy, facecolor=[0.6,0.6,0.6], edgecolor='none', zorder=0 )
            obj = objectives[6]
            pred = sample.get_predictions(obj)[0]
            meas = obj.measurements[0]
            indVars,data = meas.detrend(pred)
            plt.plot( indVars, data, c='k', zorder=1 )
            ax2.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=2 )
            ax2.set_xlim([ np.min(meas.indVars_actual),np.max(meas.indVars_actual) ])

            ax2 = plt.subplot2grid( (6,12), (4,8), colspan=2, rowspan=2 )
            yy = np.append(np.max(preds[:,4,:],axis=0),np.min(preds[:,4,:],axis=0)[::-1])
            ax2.fill( xx,yy, facecolor=[0.6,0.6,0.6], edgecolor='none', zorder=0 )
            obj = objectives[7]
            pred = sample.get_predictions(obj)[0]
            meas = obj.measurements[0]
            indVars,data = meas.detrend(pred)
            plt.plot( indVars, data, c='k', zorder=1 )
            ax2.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=2 )
            ax2.set_xlim([ np.min(meas.indVars_actual),np.max(meas.indVars_actual) ])

            ax2 = plt.subplot2grid( (6,12), (4,10), colspan=2, rowspan=2 )
            yy = np.append(np.max(preds[:,5,:],axis=0),np.min(preds[:,5,:],axis=0)[::-1])
            ax2.fill( xx,yy, facecolor=[0.6,0.6,0.6], edgecolor='none', zorder=0 )
            obj = objectives[8]
            pred = sample.get_predictions(obj)[0]
            meas = obj.measurements[0]
            indVars,data = meas.detrend(pred)
            plt.plot( indVars, data, c='k', zorder=1 )
            ax2.scatter(  meas.indVars_actual, meas.data[:,1], s=18, c='r', edgecolor='none', marker='.', zorder=2 )
            ax2.set_xlim([ np.min(meas.indVars_actual),np.max(meas.indVars_actual) ])

            plt.tight_layout()

            plt.savefig('%s/pareto_%s_pilotPoints2_%06i.eps'%(plotdir,fn_suffix,sample.id),format='eps',bbox_inches='tight' )
            plt.savefig('%s/pareto_%s_pilotPoints2_%06i.png'%(plotdir,fn_suffix,sample.id),format='png',bbox_inches='tight', dpi=600 )
            plt.close()
            #exit()
