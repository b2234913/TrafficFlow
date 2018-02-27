#!/bin/bash
url='http://tisvcloud.freeway.gov.tw/history/vd/'

dir=$1
if [ $2 -lt 10 ]; then
	dir=${dir}0$2
else
	dir=${dir}$2
fi

if [ $3 -lt 10 ]; then
	dir=${dir}0$3
else
	dir=${dir}$3
fi
url=${url}${dir}

mkdir $dir

for i in $(seq 0 23)
do
	for j in $(seq 0 5 55)
	do
		if [ $i -lt 10 ]; then
			number=0$i
		else
			number=$i
		fi
		if [ $j -lt 10 ]; then
			number=${number}0$j
		else
			number=${number}$j
		fi
		link=${url}/vd_value5_${number}.xml.gz
		echo $link
		wget -P ./${dir}/ ${link} > /dev/null 2> /dev/null
		gzip -d ./${dir}/vd_value5_${number}.xml.gz
	done
done

