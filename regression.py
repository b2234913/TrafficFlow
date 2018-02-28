# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import numpy as np

def plot(x,y,n):
	dataX = np.arange(max(x))
	coefficients = np.polyfit(y,x,n)
	if n == 2:
		trend_line = dataX*dataX *coefficients[0] + dataX*coefficients[1]+coefficients[2]
	elif n == 1:
		trend_line = dataX*coefficients[0] + coefficients[1]
	print np.argmax(trend_line)

	print coefficients
	plt.plot(x,y,'*') 
	# plt.plot(trend_line)

    # 設定圖的範圍, 不設的話，系統會自行決定
	# plt.xlim(-30,390)
	# plt.ylim(-1.5,1.5)

    # 照需要寫入x 軸和y軸的 label 以及title
	plt.xlabel("final_laneoccupy") 
	plt.ylabel("final_volume") 
	plt.title("The Title") 
    
	plt.show() 
    # 如果要存成圖形檔:
    # 把 pyplot.show() 換成下面這行:
	# plt.savefig("filename.png",dpi=300,format="png") 

def main():
	final_speed = []
	final_volume = []
	final_laneoccupy = []
	for i in range(1,2):
		filename = '../json/201801'+ str(i).zfill(2) +'.json'
		
		
		with open(filename) as f :
			data = json.load(f)
			f.close()
			# a = json.dumps(data,sort_keys=True,indent=2, separators=(',', ': '))

			for i in range(len(data)):
				for j in range(len(data[i]['data'])):
				# if data[i]['data'][j]['vdid'] == 'nfbVD-N5-N-28.420-M':
					# print 'vdid:', data[i]['data'][j]['vdid'],'status:', data[i]['data'][j]['status']
					
					if data[i]['data'][j]['status'] == 1 or data[i]['data'][j]['vdid'] != 'nfbVD-N5-N-28.420-M':
						continue
					speed = 0
					volume = 0
					laneoccupy = 0
					for k in range(len(data[i]['data'][j]['lane'])):
						# print data[i]['data'][j]['lane'][k]['vsrid']
						speed += data[i]['data'][j]['lane'][k]['speed']
						volume += data[i]['data'][j]['lane'][k]['S'] + int(data[i]['data'][j]['lane'][k]['L']*1.5) + data[i]['data'][j]['lane'][k]['T']*2
						laneoccupy += data[i]['data'][j]['lane'][k]['laneoccupy']
					
					speed = speed/len(data[i]['data'][j]['lane'])
					volume = int(volume/len(data[i]['data'][j]['lane']))
					laneoccupy = laneoccupy/len(data[i]['data'][j]['lane'])

					final_speed.append(speed)
					final_volume.append(volume)
					final_laneoccupy.append(laneoccupy)
					# print len(data[i]['data'][j]['lane'])
					# print 'speed(km/hr):',speed,'volume(veh/5min):',volume,'laneoccupy(%):',laneoccupy
				
	plot(final_laneoccupy,final_volume,2)

	print final_laneoccupy
		
		# print coefficients




if __name__ == "__main__":
	main()
	