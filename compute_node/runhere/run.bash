#!/bin/bash

source /home/ubuntu/.bashrc

PATH=/home/ubuntu/visit2_12_2.linux-x86_64/bin/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

cd /home/ubuntu/runhere

id=`echo $(curl -s http://169.254.169.254/latest/meta-data/instance-id)`
echo $id > id.txt

while true; do

rm input_files.tgz input.geo output.pkl solution_files/* solution-point*txt id_simulation
python stop_aws.py || break
python pull.py     || break
tar xvzf input-files.tgz
python add_probes.py
#/home/ubuntu/geocen/geocentric-2.0-alex/install/bin/geocentric input.geo || continue
mpiexec -n 4 /home/ubuntu/geocen/geocentric-2.0-alex/install/bin/geocentric input.geo || continue
python post_process.py
python push.py

#exit

done

#aws ec2 terminate-instance-in-auto-scaling-group --instance-id $id --should-decrement-desired-capacity
aws ec2 terminate-instances --instance-ids=$id

