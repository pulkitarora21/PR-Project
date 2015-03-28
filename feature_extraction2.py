import json
import nltk
from nltk.corpus import stopwords # Import the stop word list
import re
from urlparse import urlparse

def histogram(words, freq):
    for w in words:
        if freq.has_key(w):
            freq[w] = freq[w] + 1
        else:
            freq[w] = 1
    return freq



json_data=open('stories3_karma.txt')
data = json.load(json_data)



for i in range(0,len(data)):
    data[i]["datetime"]=data[i]["time"] # store the existing datetime (which is stored in time in the existing stories) in date 
    data[i]["time"]=data[i]["time"]%86400 # extract only the time component from unix datetime
    data[i]["time_slot"]=data[i]["time"]/1800
    try:
        data[i]["netloc"]=urlparse(data[i]["url"]).netloc # extract server name from the url - www.website.com from http://www.website.com/directory/..
    except KeyError:
        data[i]["netloc"]="" # Append null string for netloc if there isn't any url for this post
    
    try:
        text = data[i]["text"]
    except KeyError:
        text = ""
    freq = {}
    # print text
    words = re.sub("[^a-zA-Z]"," ",text )
    lower_case = words.lower()        # Convert to lower case
    words = lower_case.split() 

    words = [w for w in words if not w in stopwords.words("english")]
    freq = {}
    freq = histogram(words, freq)
    

    try:
        title = data[i]["title"]
    except KeyError:
        title = ""
    words = re.sub("[^a-zA-Z]"," ",title)
    lower_case = words.lower()        # Convert to lower case
    words = lower_case.split() 

    words = [w for w in words if not w in stopwords.words("english")]
    freq = histogram(words, freq)
    # print freq
    data[i]["words_freq"] = freq


with open('stories3_feature_extraction.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)

