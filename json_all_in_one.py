# -*- coding: utf-8 -*-
import json
def load_json(filename):
	with open(filename) as f :
		data = json.load(f)
	return data


def main():
	filename = '../json/20180101.json'
	data = load_json(filename)
	print data[0]['data']

if __name__ == "__main__":
	main()