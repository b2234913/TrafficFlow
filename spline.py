# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import numpy as np
import math
import array

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """
    return np.isnan(y), lambda z: z.nonzero()[0]

def fill_nan(y):
    y = np.asarray(y)
    nans, x= nan_helper(y)
    y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    return y

def load_json(filename):
	with open(filename) as f :
		data = json.load(f)
	return data

def json2array(data,want_time):
	want_date = '20180102'
	# want_time = '0800'
	vdid = []
	status = []
	volume = []
	speed = []
	laneoccupy = []

	for i in range(len(data)):
		if data[i] and data[i]['date'] == want_date and data[i]['time'] == want_time:
			for j in range(len(data[i]['data'])):
				if data[i]['data'][j]:
					vdid.append(data[i]['data'][j]['vdid'])
					status.append(data[i]['data'][j]['status'])
					tmp_speed = 0
					tmp_laneoccupy= 0
					for k in range(len(data[i]['data'][j]['lane'])):
						tmp_speed += data[i]['data'][j]['lane'][k]['speed']
						tmp_laneoccupy += data[i]['data'][j]['lane'][k]['laneoccupy']
					speed.append(tmp_speed/len(data[i]['data'][j]['lane']))
					laneoccupy.append(tmp_laneoccupy/len(data[i]['data'][j]['lane']))

	return  vdid, status, speed, laneoccupy, volume

def plot(x,y,x_label,y_label):
	my_dpi = 300
	
	# plt.plot(x,y,label = line_label) 
	plt.plot(x,y)

	# plt.plot(reg(x,y,2))
    # 設定圖的範圍, 不設的話，系統會自行決定
	# plt.xlim(0,max(x))
	# plt.ylim(0,max(y))

    # 照需要寫入x 軸和y軸的 label 以及title
	plt.xlabel(x_label) 
	plt.ylabel(y_label) 

	
    # 如果要存成圖形檔:
    # 把 pyplot.show() 換成下面這行:
	# plt.savefig("filename.png",dpi=300,format="png") 

def compute_travel_time(speed):
	travel_time = 0
	# length of 雪山隧道 (km)
	length = 14 
	for i in range(len(speed)):
		if i < len(speed)-1:
			travel_time += length/float(len(speed)) * 2/float(speed[i]+speed[i+1])*60
	if travel_time<0:
		travel_time = np.nan
	return travel_time

def main():			
	filename = '1.json'
	data = load_json(filename)
	my_dpi = 150
	travel_time = []
	TimeStamp = [] 
	plt.figure(figsize=(1280/my_dpi, 720/my_dpi), dpi=my_dpi)

	for j in range(0,25):
		for i in range(0,60,5):
			want_time = str(j).zfill(2) + str(i).zfill(2)
			TimeStamp.append(want_time)
			[ vdid, status, speed, laneoccupy, volume] = json2array(data,want_time)
			print speed 
			travel_time.append(compute_travel_time(speed))

			# plot(range(len(speed)),speed,'vdid','speed',want_time)
	# travel_time.scipy.interpolate()

	nans, x= nan_helper(travel_time)
	travel_time = np.asarray(travel_time)
	travel_time[nans] = np.interp(x(nans), x(~nans), travel_time[~nans])

	plot(range(len(travel_time)),travel_time,'time','travel_time')
	plt.xticks(range(0,len(travel_time),12), range(24))
	title = 'travel_time_full_day'
	plt.title(title) 
	plt.show() 
	# plt.savefig('./figure/' + title + ".png",dpi=my_dpi,format="png") 


if __name__ == "__main__":
	main()