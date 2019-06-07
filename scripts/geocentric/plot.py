import sys
sys.path.append('/home/ubuntu/poroelast9/imports/misc')
from header import *
import pickle

import tradeoffs
import forwardModels
import postProcessors
import detrend
from connect_info import *

#if not 6<datetime.datetime.now().hour<8: exit()
#if datetime.datetime.now().hour<8: exit()
#exit()

engine  = sqlalchemy.create_engine('mysql+mysqldb://%s:%s@localhost/%s'%(db_user,db_pswd,db_title), echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

opts = session.query(Optimization).all()
objs = session.query(Objective).all()

parameters = session.query(Parameter).all()

#for param in opts[0].parameters:
#  print param.get_pxd().domain.title, param.get_pxd().property.title
#exit()

#print len(opts[0].get_complete_samples())
#exit()

#ests = opts[0].misc['ests']
#print len(ests)
#exit()

#paretoRanks = start_pareto_rank_structure(opts,np.array(objs)[np.array([0,1,2,6,7,8])])
#paretoRanks = pickle.load(open('pareto.pkl','rb'))['paretoRank']

#plotting_codes.plot_pareto3b(opts,plotdir,'sims1',[[objs[0],objs[1]],[objs[1],objs[2]],[objs[0],objs[2]],[objs[1],objs[8]],[objs[0],objs[8]]],paretoRanks)

#paretoRanks = start_pareto_rank_structure(opts,np.array(objs)[np.array([0,1,2,6,7,8])])
paretoRanks = pickle.load(open('pareto.pkl','rb'))['paretoRank']

#plotting_codes.plot_data(opts,plotdir,'sims1',objs,paretoRanks,[10,15,15,999,999,999])
#plotting_codes.plot_data(opts,plotdir,'sims2',objs,paretoRanks,[999,999,999,25,30,35])
plotting_codes.plot_data(opts,plotdir,'sims3',objs,paretoRanks,[12,20,16,80,90,100])

#plotting_codes.plot_pareto_hist(opts,plotdir,'sims1',objs,paretoRanks,[10,15,15,999,999,999])
#plotting_codes.plot_pareto_hist(opts,plotdir,'sims2',objs,paretoRanks,[999,999,999,20,25,30])
#plotting_codes.plot_pareto_hist(opts,plotdir,'sims3',objs,paretoRanks,[12,20,16,60,70,80])

#plotting_codes.plot_pareto_coin(opts,plotdir,'sims1',objs,paretoRanks,[10,15,15,999,999,999])
#plotting_codes.plot_pareto_coin(opts,plotdir,'sims2',objs,paretoRanks,[999,999,999,25,30,35])
#plotting_codes.plot_pareto_coin(opts,plotdir,'sims3',objs,paretoRanks,[12,20,16,80,90,100])

#plotting_codes.plot_pareto3b(opts,plotdir,'sims',[[objs[0],objs[1]],[objs[0],objs[2]],[objs[0],objs[6]],[objs[0],objs[7]],[objs[0],objs[8]],[objs[1],objs[2]],[objs[1],objs[6]],[objs[1],objs[7]],[objs[1],objs[8]],[objs[2],objs[6]],[objs[2],objs[7]],[objs[2],objs[8]],[objs[6],objs[7]],[objs[6],objs[8]],[objs[7],objs[8]]],paretoRanks,[[4,200],[2,150],[3,400],[2,200],[3,200],[9,200]])

#paretoRanks = start_pareto_rank_structure(opts,np.array(objs)[np.array([0,1,2])])
#paretoRanks = pickle.load(open('pareto.pkl','rb'))['paretoRank']
#plotting_codes.plot_data(opts,plotdir,'sims2',objs,paretoRanks)
#plotting_codes.plot_pareto_hist(opts,plotdir,'sims2',objs,paretoRanks)
#plotting_codes.plot_pareto_coin(opts,plotdir,'sims2',objs,paretoRanks)
#plotting_codes.plot_pareto3b(opts,plotdir,'sims2',[[objs[0],objs[1]],[objs[1],objs[2]],[objs[0],objs[2]],[objs[0],objs[6]],[objs[1],objs[6]],[objs[1],objs[6]],[objs[0],objs[7]],[objs[1],objs[7]],[objs[1],objs[7]],[objs[0],objs[8]],[objs[1],objs[8]],[objs[1],objs[8]],[objs[6],objs[7]],[objs[6],objs[8]],[objs[7],objs[8]]],paretoRanks)

#paretoRanks = start_pareto_rank_structure(opts,np.array(objs)[np.array([6,7,8])])

#paretoRanks = pickle.load(open('pareto.pkl','rb'))['paretoRank']
#plotting_codes.plot_data(opts,plotdir,'sims3',objs,paretoRanks)
#plotting_codes.plot_pareto_hist(opts,plotdir,'sims3',objs,paretoRanks)
#plotting_codes.plot_pareto_coin(opts,plotdir,'sims3',objs,paretoRanks)
#plotting_codes.plot_pareto3b(opts,plotdir,'sims3',[[objs[0],objs[1]],[objs[1],objs[2]],[objs[0],objs[2]],[objs[0],objs[6]],[objs[1],objs[6]],[objs[1],objs[6]],[objs[0],objs[7]],[objs[1],objs[7]],[objs[1],objs[7]],[objs[0],objs[8]],[objs[1],objs[8]],[objs[1],objs[8]],[objs[6],objs[7]],[objs[6],objs[8]],[objs[7],objs[8]]],paretoRanks)

#plotting_codes.plot_pareto3b(opts,plotdir,'sims1',[[objs[0],objs[1]],[objs[1],objs[2]],[objs[0],objs[2]],[objs[0],objs[6]],[objs[1],objs[6]],[objs[1],objs[6]],[objs[0],objs[7]],[objs[1],objs[7]],[objs[1],objs[7]],[objs[0],objs[8]],[objs[1],objs[8]],[objs[1],objs[8]],[objs[6],objs[7]],[objs[6],objs[8]],[objs[7],objs[8]]])

#plotting_codes.plot_pareto3db(opts,plotdir,'sims1',[objs[0],objs[1],objs[2]],[objs[0],objs[1],objs[2]])
#plotting_codes.plot_pareto3db(opts,plotdir,'sims1',[objs[0],objs[1],objs[2]],[objs[6],objs[7],objs[8]])
#plotting_codes.plot_pareto3db(opts,plotdir,'sims1',[objs[0],objs[1],objs[2]],[objs[0],objs[1],objs[8]])

'''paretoRanks = start_pareto_rank_structure(opts,np.array(objs)[np.array([6,7,8])])
plotting_codes.plot_data(opts,plotdir,'sims2',objs,paretoRanks)
plotting_codes.plot_pareto_hist(opts,plotdir,'sims2',objs[0:2],paretoRanks)
plotting_codes.plot_pareto3b(opts,plotdir,'sims2',[[objs[0],objs[1]],[objs[1],objs[2]],[objs[0],objs[2]],[objs[1],objs[8]],[objs[0],objs[8]]],paretoRanks)
plotting_codes.plot_pareto3db(opts,plotdir,'sims2',[objs[6],objs[7],objs[8]],[objs[0],objs[1],objs[2]])
plotting_codes.plot_pareto3db(opts,plotdir,'sims2',[objs[6],objs[7],objs[8]],[objs[6],objs[7],objs[8]])
plotting_codes.plot_pareto3db(opts,plotdir,'sims2',[objs[6],objs[7],objs[8]],[objs[0],objs[1],objs[8]])
plotting_codes.plot_pareto_coin(opts,plotdir,'sims2',objs[0:2],paretoRanks)

paretoRanks = start_pareto_rank_structure(opts,np.array(objs)[np.array([0,1,2,6,7,8])])
plotting_codes.plot_data(opts,plotdir,'sims3',objs,paretoRanks)
plotting_codes.plot_pareto_hist(opts,plotdir,'sims3',objs[0:2],paretoRanks)
plotting_codes.plot_pareto3b(opts,plotdir,'sims3',[[objs[0],objs[1]],[objs[1],objs[2]],[objs[0],objs[2]],[objs[1],objs[8]],[objs[0],objs[8]]],paretoRanks)
plotting_codes.plot_pareto3db(opts,plotdir,'sims3',[objs[0],objs[1],objs[2],objs[6],objs[7],objs[8]],[objs[0],objs[1],objs[2]])
plotting_codes.plot_pareto3db(opts,plotdir,'sims3',[objs[0],objs[1],objs[2],objs[6],objs[7],objs[8]],[objs[6],objs[7],objs[8]])
plotting_codes.plot_pareto3db(opts,plotdir,'sims3',[objs[0],objs[1],objs[2],objs[6],objs[7],objs[8]],[objs[0],objs[1],objs[8]])
plotting_codes.plot_pareto_coin(opts,plotdir,'sims3',objs[0:2],paretoRanks)'''

#plotting_codes.plot_pareto3d(opts,plotdir,'sims1',[[objs[0],objs[1],objs[2]]],paretoRanks)
#plotting_codes.plot_pareto2(opts,plotdir,'sims1',objs[0:2],paretoRanks)
#plotting_codes.plot_pareto_coin(opts,plotdir,'sims1',objs[0:2],paretoRanks)
#plotting_codes.plot_pareto_ellipse(opts,plotdir,'sims1',objs[0:2],paretoRanks)
#plotting_codes.plot_pareto2b(opts,plotdir,'sims1',objs[0:2],paretoRanks)

#plotting_codes.plot_pxd2d(opts,plotdir,'sims1')
#except: pass

session.commit()
