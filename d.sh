#!/bin/sh 
year=2018
mon=1
for day in $(seq 1 31)
do
	sh download.sh $year $mon $day
done
