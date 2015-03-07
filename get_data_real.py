import json, pycurl, StringIO
base = 8757260
arrayOfStories = []
arrayOfComments = []
arrayOfPolls = []
arrayOfJobs = []
arrayOfPollopts = []
noOfPostsToBeScanned = 20000
for i in range(1,noOfPostsToBeScanned):
	currentID = base - i
	url = "https://hacker-news.firebaseio.com/v0/item/"+str(currentID)+".json"
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
	print currentID
	print data1
	print data1==None
	if data1!=None:
		print "here"
	else:
		print "yo :D"
		continue
	print data1["type"]=="story"
	if(data1["type"]):
		if(data1["type"])=="story":
			arrayOfStories.append(data1)
		if(data1["type"])=="comment":
			arrayOfComments.append(data1)
		if(data1["type"])=="poll":
			arrayOfPolls.append(data1)
		if(data1["type"])=="job":
			arrayOfJobs.append(data1)
		if(data1["type"])=="pollopt":
			arrayOfPollopts.append(data1)
	print len(arrayOfStories)
	print currentID
	with open('stories.txt', 'w') as outfile:
		json.dump(arrayOfStories, outfile)
	with open('comments.txt', 'w') as outfile:
		json.dump(arrayOfComments, outfile)

	with open('polls.txt', 'w') as outfile:
		json.dump(arrayOfPolls, outfile)

	with open('jobs.txt', 'w') as outfile:
		json.dump(arrayOfPolls, outfile)

	with open('pollopts.txt', 'w') as outfile:
		json.dump(arrayOfPollopts, outfile)
#9158271

with open('stories.txt', 'w') as outfile:
    json.dump(arrayOfStories, outfile)

with open('comments.txt', 'w') as outfile:
    json.dump(arrayOfComments, outfile)

with open('polls.txt', 'w') as outfile:
    json.dump(arrayOfPolls, outfile)

with open('jobs.txt', 'w') as outfile:
    json.dump(arrayOfPolls, outfile)

with open('pollopts.txt', 'w') as outfile:
    json.dump(arrayOfPollopts, outfile)