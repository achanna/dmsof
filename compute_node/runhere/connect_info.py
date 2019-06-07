import paramiko

db_addr  = 'localhost'
db_user  = 'remote'
db_pswd  = 'geomech173'
db_title = 'avant176'

host_addr = db_addr
host_user = 'ubuntu'
host_key  = paramiko.RSAKey.from_private_key_file('/home/ubuntu/.ssh/aws_poro.pem')

aws_id    = 'temp'
aws_key   = 'temp'
bucket    = db_title
