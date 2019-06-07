#!/bin/bash

for i in {1..50}
do

python maintain.py || exit
python plot.py || exit
python stop.py || exit

done
