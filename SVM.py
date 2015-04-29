from sklearn import svm 
import numpy as np
import matplotlib.pyplot as mp
import json
from sklearn.metrics import roc_curve, auc
import pylab as pl


def loadData(fileName):
	#Loading data
	json_data=open(fileName)
	data = json.load(json_data)
	return data

def rejectData(data):
	dataNew = []
	for i in range(0, len(data)):
		try:
			score = data[i]["score"]
			dataNew.append(data[i])
		except KeyError:
			#Do nothing
			doNothing = 1
			
	return dataNew

def getDictionary(data):
	#Make a list of all words
	words = []
	for i in range(0,len(data)):
		for word in data[i]["words_freq_stem"]:
			words.append(word)

	# print words
	return words


def getUsers(features):
	#Make a list of all users
	users = []
	for id in features:
		users.append(id)
	return users




def getFeatures(words, data):
	features = {}
	classes = {}
	scoreNotPresent = 0
	class1 = 0
	for i in range(0,len(data)):
		features[data[i]["id"]] = [data[i]["time_slot"], data[i]["user_karma"]]
		try:
			if data[i]["score"]>50:
				classes[data[i]["id"]] = 1
				class1 = class1 + 1
			else:
				classes[data[i]["id"]] = 0
		except KeyError:
			scoreNotPresent = scoreNotPresent + 1
			print "------------------------SCORE NOT PRESENT :(-------------------------------------------"
	print scoreNotPresent
	print "-------------------------------Samples with class1: ",class1,"---------------------"
	return features, classes, class1


def getNumpyArrays(features, classes, users):
	featuresList = []
	classesList = []
	for i in range(len(users)):
		featuresList.append(features[users[i]])
		classesList.append(classes[users[i]])

	featuresArray = np.array(featuresList)
	classesArray = np.array(classesList)
	return featuresArray, classesArray


def evaluate2(svmObj, featuresArray, classesArray):
	predictedProb = svmObj.predict_proba(featuresArray)
	print "------------------PROBABILITIES PREDICTED----------------"
	print predictedProb
	
	fpr, tpr, thresholds = roc_curve(classesArray, predictedProb[:, 1])
	roc_auc = auc(fpr, tpr)
	print "Area under the ROC curve : %f" % roc_auc

	pl.clf()
	pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
	pl.xlim([0.0, 1.0])
	pl.ylim([0.0, 1.0])
	pl.xlabel('False Positive Rate')
	pl.ylabel('True Positive Rate')
	pl.title('Receiver operating characteristic example')
	pl.legend(loc="lower right")
	pl.show()

def evaluate(svmObj, featuresArray, classesArray):
	totalPredictions = 0
	correctPredictions = 0
	predicted1 = 0
	predicted0 = 0
	TruePositives = 0 
	TrueNegatives = 0 
	FalsePositives = 0 
	FalseNegatives = 0
	for i in range(0, len(featuresArray)):
		trueClass = classesArray[i]
		predictedClass = svmObj.predict(featuresArray[i])
		totalPredictions = totalPredictions + 1
		if trueClass == predictedClass:
			correctPredictions = correctPredictions + 1
			if trueClass == 1:
				TruePositives = TruePositives + 1
			else:
				TrueNegatives = TrueNegatives + 1
		else:
			if predictedClass == 1:
				FalsePositives = FalsePositives + 1
			else:
				FalseNegatives = FalseNegatives + 1
		if predictedClass == 1:
			predicted1 = predicted1 + 1
			# print "---------------------------1----------------------------"
		else:
			predicted0 = predicted0 + 1
			# print "---------------------------0----------------------------"
	print "Number of 1s predicted: ", predicted1, " and number of 0s predicted: ", predicted0
	print "TPR: ", (float(TruePositives))/(TruePositives+FalseNegatives), " FPR: ", (float(FalsePositives))/(FalsePositives+TrueNegatives)
	return correctPredictions/float(totalPredictions)


def equalizeClasses(features, classes, class1):
	class0 = 0
	featuresNew = {}
	classesNew = {}
	for id in features:
		if classes[id] == 0:
			class0 = class0 + 1
			if class0 <= class1:
				featuresNew[id] = features[id]
				classesNew[id] = classes[id]
		else:
			featuresNew[id] = features[id]
			classesNew[id] = classes[id]
	return featuresNew, classesNew



trainingData = loadData("stories2_feature_extraction.txt")
trainingData = rejectData(trainingData)
trainingWords = getDictionary(trainingData)
trainingFeatures, trainingClasses, class1 = getFeatures(trainingWords, trainingData)
trainingFeatures, trainingClasses = equalizeClasses(trainingFeatures, trainingClasses, class1)
print "==========================", len(trainingFeatures),"======================"
trainingUsers = getUsers(trainingFeatures)
trainingFeaturesArray, trainingClassesArray = getNumpyArrays(trainingFeatures, trainingClasses, trainingUsers)


clf = svm.SVC(kernel='linear', degree=2, C = 1.0, probability=True)
print "----------------------BEFORE TRAINING----------------------"
clf.fit(trainingFeaturesArray, trainingClassesArray)
#print(clf.predict([0.58,0.76]))
print "------------------------TRAINING DONE----------------------"


testingData = loadData("stories3_feature_extraction.txt")
testingData = rejectData(testingData)
testingWords = getDictionary(testingData)
testingFeatures, testingClasses, testingClass1 = getFeatures(testingWords, testingData)
testingUsers = getUsers(testingFeatures)
testingFeaturesArray, testingClassesArray = getNumpyArrays(testingFeatures, testingClasses, testingUsers)
print "-------------------------BEFORE EVALUATION----------------"
evaluate2(clf, testingFeaturesArray, testingClassesArray)
print "-------------------------EVALUATION DONE------------------"