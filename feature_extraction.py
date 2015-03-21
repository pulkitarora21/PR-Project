import json
from urlparse import urlparse

json_data=open('stories1.txt')
data = json.load(json_data)

for i in range(0,len(data)):
	data[i]["datetime"]=data[i]["time"] # store the existing datetime (which is stored in time in the existing stories) in date 
	data[i]["time"]=data[i]["time"]%86400 # extract only the time component from unix datetime
	try:
		data[i]["netloc"]=urlparse(data[i]["url"]).netloc # extract server name from the url - www.website.com from http://www.website.com/directory/..
	except KeyError:
		data[i]["netloc"]="" # Append null string for netloc if there isn't any url for this post


with open('stories1_feature_extraction.txt', 'w') as outfile:
	json.dump(data, outfile, indent=4)

