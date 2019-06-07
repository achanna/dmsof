import paramiko

db_addr  = 'localhost'
db_user  = 'remote'
db_pswd  = 'geomech173'
db_title = 'soecalcpi'

host_addr = db_addr
host_user = 'ubuntu'
host_pkey = paramiko.RSAKey.from_private_key_file('/home/achanna/.ssh/aws_poro.pem')

aws_id    = 'temp'
aws_key   = 'temp'
bucket    = db_title

datadir   = '/home/achanna/poroelast9/data/calcpi'
plotdir   = '/home/achanna/poroelast9/images/calcpi'
