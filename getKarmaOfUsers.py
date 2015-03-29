import json, pycurl, StringIO
from urlparse import urlparse

json_data=open('stories3.txt')
data = json.load(json_data)
username = ""
for i in range(0,len(data)):
	try:
		username = str(data[i]["by"])
	except KeyError:
		data[i]["user_karma"] = 0
		data[i]["user_avg_karma"] = 0
		continue
	url = "https://hacker-news.firebaseio.com/v0/user/"+username+".json"
	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.SSL_VERIFYPEER, 0)
	c.setopt(pycurl.SSL_VERIFYHOST, 0)
	b = StringIO.StringIO()
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.setopt(pycurl.FOLLOWLOCATION, 1)
	c.setopt(pycurl.MAXREDIRS, 5)
	c.perform()
	htmlsrc = b.getvalue()

	json_data=htmlsrc
	data1 = json.loads(json_data)
	try:
		data[i]["user_karma"] = data1["karma"]
		data[i]["user_avg_karma"] = (data1["karma"])/(float(len(data1["submitted"])))
	except KeyError:
		data[i]["user_karma"] = 0
		data[i]["user_avg_karma"] = 0

	print data[i]


with open('stories3_karma.txt', 'w') as outfile:
	json.dump(data, outfile, indent=4)
