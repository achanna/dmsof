#!/bin/bash

while true ; do

python elitism.py
python maintain.py || exit
python plot.py
python stop.py || exit

done
