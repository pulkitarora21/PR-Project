import json, pycurl, StringIO
url = "https://hacker-news.firebaseio.com/v0/user/jl.json"
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
data = json.loads(json_data)
print data