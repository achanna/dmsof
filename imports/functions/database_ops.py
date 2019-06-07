import sys
sys.path.append('../imports/misc')
from header import *

def connectDB(addr,user,pswd,title=None):
  con = MySQLdb.connect( addr, user, pswd )
  cur = con.cursor()
  if title!=None: cur.execute("USE %s" % title)
  return con,cur

def createDB(con,cur,title):
  cur.execute("SHOW DATABASES LIKE '%s'" % title)
  if len(cur.fetchall())>0: pass
  else:
    cur.execute("CREATE DATABASE %s" % title)
    con.commit()

def deleteDB(con,cur,title):
  cur.execute("SHOW DATABASES LIKE '%s'" % title)
  if len(cur.fetchall())>0:
    cur.execute("DROP DATABASE IF EXISTS %s" % title)
    con.commit()

def deleteTables(con,cur,title):
  cur.execute("USE %s" % title)
  cur.execute("UNLOCK TABLES")
  cur.execute("SHOW TABLES")
  output=cur.fetchall()
  for i in range(len(output)): cur.execute("TRUNCATE %s"%output[i][0])
  for i in range(len(output)): cur.execute("TRUNCATE %s"%output[i][0])
  for i in range(len(output)): cur.execute("TRUNCATE %s"%output[i][0])
  for i in range(len(output)): cur.execute("DROP TABLE %s"%output[i][0])
  con.commit()

def emptyDB(con,cur,title):
  cur.execute("USE %s" % title)
  cur.execute("SHOW TABLES")
  output=cur.fetchall()
  for i in range(len(output)):
    cur.execute("TRUNCATE %s"%output[i][0])
  con.commit()
