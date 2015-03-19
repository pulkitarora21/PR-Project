import json
json_data=open('stories1.txt')

data = json.load(json_data)
with open('stories1_pretty.txt', 'w') as outfile:
	json.dump(data, outfile, indent=4)