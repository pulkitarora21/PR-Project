import json
json_data=open('stories1.txt')
data = json.load(json_data)

for i in range(0,len(data)):
	data[i]["time"]=data[i]["time"]%86400

with open('stories1_feature_extraction.txt', 'w') as outfile:
	json.dump(data, outfile, indent=4)

