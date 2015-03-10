import json
from pprint import pprint
json_data=open('stories2.txt')

data = json.load(json_data)
print len(data)
json_data.close()
