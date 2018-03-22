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
    return speed, laneoccupy, flow

def plot(x,y,x_label,y_label):

    
    # plt.plot(x,y,label = line_label) 
    plt.plot(x,y)

    # plt.xlim(0,max(x))
    plt.ylim(0,110)

    plt.xlabel(x_label) 
    plt.ylabel(y_label) 
    

def main():
    filename = '1.json'
    data = load_json(filename)

    vdid = want_vdid[1]
    want_date = '20180101'

    my_dpi = 150
    plt.figure(figsize=(1280/my_dpi, 720/my_dpi), dpi=my_dpi)
    for n in range(1,8):
        want_date = '201801' + str(n).zfill(2)
        speed_array = []
        laneoccupy_array = []
        flow_array = []
        for i in range(0,24,1):
            for j in range(0,60,5):
                want_time = str(i).zfill(2) + str(j).zfill(2)
                print want_time
                speed, laneoccupy, flow = data2array(data,vdid,want_date,want_time)
                speed_array.append(speed)
                laneoccupy_array.append(laneoccupy)
                flow_array.append(flow)

        speed_array = fill_nan(speed_array)
        laneoccupy_array = fill_nan(laneoccupy_array)
        flow_array = fill_nan(flow_array)

        



 
        # title = 'velocity-time_plot_' + want_date + '_' + vdid
        title = 'velocity-time_plot_' + '20180101-20180107' + vdid 


        # title_figure = title + '_' + want_vdid
        # plot location speed plot
        plot(range(len(speed_array)),speed_array,'time','velocity')
        plt.xticks(range(0,len(speed_array),12), range(24))
        plt.title(title)
        # plt.show()


        # travel_time = compute_travel_time(speed_array)





    plt.savefig('./figure/' + title + ".png",dpi=my_dpi,format="png") 


if __name__ == "__main__":
    main()