import sys
sys.path.append('/home/achanna/Dropbox/poroelast7/imports/misc')
from header import *

def exx(stuff): return 0
def eyy(stuff): return 0
def exy(stuff): return 0

def general_multiobjective(db,output,id_simulation):
  id_datasets = output['id_datasets']
  for i in range(len(id_datasets)):
    id_dataset = id_datasets[i]
    output_interpolated = output[id_dataset]
    query = 'UPDATE Dataset SET observation=%s WHERE id=%s'
    db.cur.execute( query, (pickle.dumps(output_interpolated),id_dataset) )
    db.con.commit()
  query = 'UPDATE Simulation SET output=%s WHERE id=%s'
  db.cur.execute( query, ('output_%i'%int(id_simulation),int(id_simulation)) )
  db.con.commit()
