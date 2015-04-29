import json
json_data=open('stories3.txt')

data = json.load(json_data)
with open('stories3_pretty.txt', 'w') as outfile:
	json.dump(data, outfile, indent=4)