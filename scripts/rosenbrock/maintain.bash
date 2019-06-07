#!/bin/bash

for i in {1..1000}
do

python maintain.py || exit
python plot.py || exit
python stop.py || exit

done
