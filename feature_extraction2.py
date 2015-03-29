import json
from nltk.corpus import stopwords # Import the stop word list
import re
from urlparse import urlparse
from nltk import *
from nltk.stem.wordnet import *

def histogram(words, freq):
    for w in words:
        if freq.has_key(w):
            freq[w] = freq[w] + 1
        else:
            freq[w] = 1
    return freq


def convertToLowerRemNonAlphaChars(text):
    text = re.sub("[^a-zA-Z]"," ",text)
    text = text.lower()
    return text


def convertToLowerAndSplit(text):
    words = re.sub("[^a-zA-Z]"," ",text)
    lower_case = words.lower()        # Convert to lower case
    words = lower_case.split() 
    return words


def removeStopwords(words):
    words = [w for w in words if not w in stopwords.words("english")]
    return words

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

wnl = WordNetLemmatizer()
def lemmatizeWord(word):
    wordPos = pos_tag(word_tokenize(word))[0][1]
    wordWordnet = get_wordnet_pos(wordPos)
    if wordWordnet!='':
        word = wnl.lemmatize(word,wordWordnet)
    else:
        word = wnl.lemmatize(word)
    return word

def lemmatizeWords(words):
    words = [lemmatizeWord(word) for word in words]
    return words


def lemmatizeText(text):
    wordsPos = pos_tag(word_tokenize(text))
    words = []
    for wordPos in wordsPos:
        if get_wordnet_pos(wordPos[1])!='':
            words.append(wnl.lemmatize(wordPos[0],get_wordnet_pos(wordPos[1])))
        else:
            words.append(wnl.lemmatize(wordPos[0]))
    # words = [wnl.lemmatize(wordPos[0],get_wordnet_pos(wordPos[1])) if get_wordnet_pos(wordPos[1])!='' else wnl.lemmatize(wordPos[0]) for wordPos in wordsPos]
    return words


print lemmatizeWord("going")


print lemmatizeText("hey, he is going to school for attending classes")


json_data=open('stories1_karma.txt')
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
    

    # convert text to lower case, split it into words, remove stopwords, and add the left out words to the histogram 
    text = convertToLowerRemNonAlphaChars(text)
    # words = convertToLowerAndSplit(text) 
    # words = removeStopwords(words)
    words = lemmatizeText(text)
    words = removeStopwords(words)
    freq = {}
    freq = histogram(words, freq)
    

    try:
        title = data[i]["title"]
    except KeyError:
        title = ""
    
    # convert title to lower case, split it into words, remove stopwords, and add the left out words to the histogram 
    title = convertToLowerRemNonAlphaChars(title)
    # words = convertToLowerAndSplit(title)
    # words = removeStopwords(words)
    words = lemmatizeText(title)
    words = removeStopwords(words)
    freq = histogram(words, freq)
    

    data[i]["words_freq"] = freq


with open('stories1_feature_extraction.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)

