import json, pycurl, StringIO
base = 8757260
arrayOfStories = []
arrayOfComments = []
arrayOfPolls = []
arrayOfJobs = []
arrayOfPollopts = []
noOfPostsToBeScanned = 20000
for i in range(1,noOfPostsToBeScanned):
	with open('currentID.txt') as outfile:
		currentIDFromFile = int(outfile.readline())
	#currentIDFromFile = open('currentID.txt')
	currentID = currentIDFromFile - 1
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
	try:
		print data1["type"]
	except KeyError:
		continue
	if(data1["type"]):
		if(data1["type"])=="story":
			with open('stories2.txt') as outfile:
				print "changing arrayOfStories"
				arrayOfStories = json.load(outfile)
			arrayOfStories.append(data1)
			with open('stories2.txt', 'w') as outfile:
				json.dump(arrayOfStories, outfile)
		if(data1["type"])=="comment":
			with open('comments2.txt') as outfile:
				arrayOfComments = json.load(outfile)
			arrayOfComments.append(data1)
			with open('comments2.txt', 'w') as outfile:
				json.dump(arrayOfComments, outfile)
		if(data1["type"])=="poll":
			with open('polls2.txt') as outfile:
				arrayOfPolls = json.load(outfile)
			arrayOfPolls.append(data1)
			with open('polls2.txt', 'w') as outfile:
				json.dump(arrayOfPolls, outfile)
		if(data1["type"])=="job":
			with open('jobs2.txt') as outfile:
				arrayOfJobs = json.load(outfile)
			arrayOfJobs.append(data1)
			with open('jobs2.txt', 'w') as outfile:
				json.dump(arrayOfPolls, outfile)

		if(data1["type"])=="pollopt":
			with open('pollopts2.txt') as outfile:
				arrayOfPollopts = json.load(outfile)
			arrayOfPollopts.append(data1)
			with open('pollopts2.txt', 'w') as outfile:
				json.dump(arrayOfPollopts, outfile)
	print len(arrayOfStories)
	print currentID
	with open('currentID.txt', 'w') as outfile:
		json.dump(currentID, outfile)
	
	

	

	
	
#9158271
