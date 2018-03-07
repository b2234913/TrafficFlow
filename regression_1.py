# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import numpy as np
import inspect, re

def varname(p):
  for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
    m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
      return m.group(1)

def load_json(filename):
	with open(filename) as f :
		data = json.load(f)
	return data

def data2array(data):
	speed = []
	laneoccupy = []
	volume = []
	for i in range(len(data)):
		if data[i]:
			# print data[i]['date'],data[i]['time']
			for j in range(len(data[i]['data'])):
				if j == 0:
					# print data[i]['data'][j]['vdid'], data[i]['data'][j]['status']
					if data[i]['data'][j]['status']==0:
						speed_tmp = 0
						laneoccupy_tmp = 0
						volume_tmp = 0
						for k in range(len(data[i]['data'][j]['lane'])):
							speed_tmp += data[i]['data'][j]['lane'][k]['speed']
							laneoccupy_tmp += data[i]['data'][j]['lane'][k]['laneoccupy']
							# S 小型車 1 L 大型車 1.5 T 聯結車 2 小客車當量加權
							volume_tmp += data[i]['data'][j]['lane'][k]['S']+data[i]['data'][j]['lane'][k]['L']*1.5+data[i]['data'][j]['lane'][k]['T']*2
						speed.append(speed_tmp/len(data[i]['data'][j]['lane']))
						laneoccupy.append(laneoccupy_tmp/len(data[i]['data'][j]['lane']))
						volume.append(int(volume_tmp/len(data[i]['data'][j]['lane'])))
		else :
			continue
			# print 'data is null'
	return speed,laneoccupy,volume

def plot(x,y,x_label,y_label):

	plt.plot(x,y,'.') 

    # 設定圖的範圍, 不設的話，系統會自行決定
	# plt.xlim(-30,390)
	# plt.ylim(-1.5,1.5)

    # 照需要寫入x 軸和y軸的 label 以及title
	plt.xlabel(x_label) 
	plt.ylabel(y_label) 
	plt.title("The Title") 
    
	plt.show() 
    # 如果要存成圖形檔:
    # 把 pyplot.show() 換成下面這行:
	# plt.savefig("filename.png",dpi=300,format="png") 


def main():
	filename = '1.json'
	data = load_json(filename)
	[speed,laneoccupy,volume] = data2array(data)
	
	plot(speed,laneoccupy,'speed','laneoccupy')



if __name__ == "__main__":
	main()