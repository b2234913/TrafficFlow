# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import numpy as np
import math
import array
want_vdid=[
           'nfbVD-N5-N-15.488-M',
           'nfbVD-N5-N-16.196-M',
           'nfbVD-N5-N-16.900-M-PS',
           'nfbVD-N5-N-17.608-M',
           'nfbVD-N5-N-18.313-M-PS',
           'nfbVD-N5-N-19.012-M',
           'nfbVD-N5-N-19.689-M-PS',
           'nfbVD-N5-N-20.412-M',
           'nfbVD-N5-N-21.055-M-PS',
           'nfbVD-N5-N-21.808-M',
           'nfbVD-N5-N-22.510-M-PS',
           'nfbVD-N5-N-23.209-M',
           'nfbVD-N5-N-23.911-M-PS',
           'nfbVD-N5-N-24.677-M',
           'nfbVD-N5-N-25.310-M-PS',
           'nfbVD-N5-N-26.007-M',
           'nfbVD-N5-N-26.705-M-PS',
           'nfbVD-N5-N-27.468-M',
           'nfbVD-N5-N-27.779-M',
           'nfbVD-N5-N-28.420-M',
           'nfbVD-N5-N-29.000-M',
           'nfbVD-N5-N-29.600-M',
           'nfbVD-N5-N-30.000-I-SN',
           'nfbVD-N5-N-30.100-M'
           ];
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

def plot(x,y,x_label,y_label):
    # plt.plot(x,y,label = line_label) 
    plt.plot(x,y,'.')
    plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    plt.xlabel(x_label) 
    plt.ylabel(y_label) 

def data2array(data,want_vdid,want_date,want_time):
    speed = np.nan
    laneoccupy = np.nan
    flow = np.nan
    for i in range(len(data)):
        if data[i] and data[i]['date'] == want_date and data[i]['time'] == want_time:
            for j in range(len(data[i]['data'])):
                if data[i]['data'][j]['vdid'] == want_vdid:
                    if data[i]['data'][j]['status'] == 0:
                        data[i]['data'][j]['status']
                        tmp_speed = 0
                        tmp_laneoccupy= 0
                        tmp_flow= 0
                        weight = 0
                        a = 0
                        for k in range(len(data[i]['data'][j]['lane'])): 
                            tmp_laneoccupy += data[i]['data'][j]['lane'][k]['laneoccupy'] #五分鐘平均車道佔有百分比
                            tmp_flow += data[i]['data'][j]['lane'][k]['S'] #五分鐘小客車流量
                            tmp_flow += data[i]['data'][j]['lane'][k]['L']*1.5 #五分鐘大型車流量
                            tmp_flow += data[i]['data'][j]['lane'][k]['T']*2 #五分鐘聯結車流量
                            weight = data[i]['data'][j]['lane'][k]['S']+data[i]['data'][j]['lane'][k]['L']+data[i]['data'][j]['lane'][k]['T']
                            a += weight  
                            tmp_speed += data[i]['data'][j]['lane'][k]['speed']*weight
                            tmp_laneoccupy += data[i]['data'][j]['lane'][k]['laneoccupy']*weight
                        if a!=0:
                            speed = tmp_speed/a
                            laneoccupy = tmp_laneoccupy/a
                            flow = int(tmp_flow) #int(tmp_flow/len(data[i]['data'][j]['lane']))
                            return speed, laneoccupy, flow
                        else:
                        	speed = 0
                        	laneoccupy = 0
                        	flow = 0
                        	return speed, laneoccupy, flow
    return speed, laneoccupy, flow

def main():
  filename = '1.json'
  # want_date = '20180103'
  data = load_json(filename)
  for m in range(5):
    print m
    vdid = want_vdid[m] 
    speed_one_vdid = []
    laneoccupy_one_vdid = []
    flow_one_vdid = []
    for a in range(1,32):
      want_date = '201801' + str(a).zfill(2)
      for i in range(24):
        for j in range(0,60,5):
          want_time = str(i).zfill(2) + str(j).zfill(2)
          speed, laneoccupy, flow = data2array(data,vdid,want_date,want_time)
          speed_one_vdid .append(speed)
          laneoccupy_one_vdid.append(laneoccupy)
          flow_one_vdid.append(flow)
    # print speed_one_vdid 
    speed_one_vdid = fill_nan(speed_one_vdid)
    laneoccupy_one_vdid = fill_nan(laneoccupy_one_vdid)
    flow_one_vdid = fill_nan(flow_one_vdid)
    # print speed_one_vdid


    my_dpi = 150
    plt.figure(figsize=(1280/my_dpi, 720/my_dpi), dpi=my_dpi)
    title = 'occupy_velocity_' + want_date + '_' + '_' + vdid
    plot(laneoccupy_one_vdid,speed_one_vdid,'occupy','velocity')
    # plt.xticks(range(0,len(travel_time)+1,12), range(24))
    plt.title(title)
    plt.savefig('./figure/' + title + ".png",dpi=my_dpi,format="png") 


    plt.figure(figsize=(1280/my_dpi, 720/my_dpi), dpi=my_dpi)
    title = 'velocity_flow_' + want_date + '_' + '_' + vdid
    plot(speed_one_vdid,flow_one_vdid,'velocity','flow')
    # plt.xticks(range(0,len(travel_time)+1,12), range(24))
    plt.title(title)
    plt.savefig('./figure/' + title + ".png",dpi=my_dpi,format="png") 


    plt.figure(figsize=(1280/my_dpi, 720/my_dpi), dpi=my_dpi)
    title = 'occupy_flow_' + want_date + '_'  + '_' + vdid
    plot(laneoccupy_one_vdid,flow_one_vdid,'occupy','flow')
    # plt.xticks(range(0,len(travel_time)+1,12), range(24))
    plt.title(title)
    plt.savefig('./figure/' + title + ".png",dpi=my_dpi,format="png") 


if __name__ == "__main__":
    main()