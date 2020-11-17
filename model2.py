import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd
#from sklearn.cluster import KMeans
import numpy as np

map_labels={"bribery":0,"corruption":1,"defamation":2,"fraud":3,"scam":4 ,"defaulter":5,"none":6}
list_articles=[]
list_article_label=[]
articles=[]
frequency=[0,0,0,0,0,0,0]
X_train=[]
X_test=[]
y_train=[]
y_test=[]

with open("articles.txt", "rb") as fp:   # Unpickling
    list_articles = pickle.load(fp)
with open("articles_labels.txt", "rb") as fp:   # Unpickling
    list_article_label = pickle.load(fp)

for i in range(0,len(list_article_label)):
    list_article_label[i]=map_labels[list_article_label[i]]
    #print(list_article_label[i])
    frequency[list_article_label[i]]+=1

print([len(list_articles),len(list_articles)])
print(frequency)
for i in range(0,len(frequency)):
    frequency[i]*=0.8
    frequency[i]=int(frequency[i])

print(frequency)
for x,y in zip(list_articles,list_article_label):
    if(frequency[y]>0):
        X_train.append(x)
        y_train.append(y)
        frequency[y]-=1
    else:
        X_test.append(x)
        y_test.append(y)


#print([len(X_train),len(X_test)])
#for t in y_test:
#    if t>=1 and t<6:
#        print (t);
#print(set(y_test) - set(y_train))
#print( set(y_train) - set(y_test))

cv = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True, stop_words='english')
X_train_cv = cv.fit_transform(X_train)
X_test_cv = cv.transform(X_test)


naive_bayes = MultinomialNB()
naive_bayes.fit(X_train_cv, y_train)
predictions = naive_bayes.predict(X_test_cv)

print('Accuracy score: ', accuracy_score(y_test, predictions))
print('Precision score: ', precision_score(y_test, predictions,average=None, labels=np.unique(y_test) ))
print('Recall score: ', recall_score(y_test, predictions,average=None, labels=np.unique(y_test)))
