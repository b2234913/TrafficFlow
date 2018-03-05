# -*- coding: utf-8 -*-
import os 
import sys
import json
from xml.dom import minidom
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



def writeToJSONFile(path, fileName, data):
	filePathNameWExt =  path + '/' + fileName + '.json'
	with open(filePathNameWExt, 'w') as fp:
		json.dump(data, fp)

def get_data_form_xml(filename):	
	dataset = []
	with open(filename) as f :
		xml = minidom.parseString(f.read()).getElementsByTagName('Info')
		for i in range(len(xml)) :
			data = {}
			vdid = xml[i].attributes['vdid'].value
			status = xml[i].attributes['status'].value
			data['vdid'] = vdid.encode("utf-8")
			data['status'] = int(status)
			lanes = xml[i].getElementsByTagName('lane')
			lane = []
			for k in range(len(lanes)):
				lane_data = {}
				vsrid = lanes[k].attributes['vsrid'].value
				speed = lanes[k].attributes['speed'].value
				laneoccupy = lanes[k].attributes['laneoccupy'].value
				lane_data['vsrid'] = int(vsrid)
				lane_data['speed'] = int(speed)
				lane_data['laneoccupy'] = int(laneoccupy)
				cars = lanes[k].getElementsByTagName('cars')

				for l in range(len(cars)):					
					carid = cars[l].attributes['carid'].value.encode("utf-8")
					volume = cars[l].attributes['volume'].value
					lane_data[carid] = int(volume)
				lane.append(lane_data)
			data['lane'] = lane
			for m in range(len(want_vdid)):
				if want_vdid[m] == data['vdid']:
					dataset.append(data)
	return dataset


def main():
	# full_dataset['time'] = 
    # filename = "../20180101/vd_value5_0000.xml"
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    for n in range(start,end+1):
        date = '201801' + str(n).zfill(2)
        final_data = [] 
        for j in range(0,24,1):
            for i in range(0,60,5):
                full_dataset = {}
                time = str(j).zfill(2) + str(i).zfill(2)
                filename = '../' + date + '/vd_value5_' + time + '.xml'
                if os.path.isfile(filename) == True:
                    full_dataset['data'] = get_data_form_xml(filename)
                    full_dataset['time'] = time
                    final_data.append(full_dataset)
	writeToJSONFile('../json',date,final_data)
	

if __name__ == "__main__":
	main()
