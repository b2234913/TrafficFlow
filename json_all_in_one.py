# -*- coding: utf-8 -*-
import json
import uniout

def load_json(filename):
	with open(filename) as f :
		data = json.load(f)
	return data

def writeToJSONFile(path, fileName, data):
	filePathNameWExt =  path + '/' + fileName + '.json'
	with open(filePathNameWExt, 'w') as fp:
		json.dump(data, fp)


def main():
	day = []
	for i in range(1,32):
		filename = '../json/201801' + str(i).zfill(2) + '.json'
		print filename
		
		date = filename.split('/')[-1].split('.')[0]
		tmp = load_json(filename)

		
		for i in range(len(tmp)):
			time = tmp[i]['time']
			print time
			day_data = {}
			for j in range(len(tmp[i]['data'])):
				day_data['date'] = date
				day_data['time'] = time
				day_data['data'] = tmp[i]['data']
			day.append(day_data)

	writeToJSONFile('./','1',day)
			
if __name__ == "__main__":
	main()