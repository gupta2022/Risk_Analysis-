import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score,f1_score
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import numpy as np



def train(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1,shuffle=2)
    print(len(X),len(X_train))
    gnb = GaussianNB()
    cv = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True, stop_words='english')
    X_train_cv = cv.fit_transform(X_train).todense()
    X_test_cv = cv.transform(X_test).todense()
    predictions = gnb.fit(X_train_cv, y_train).predict(X_test_cv) #predict_proba
    c1=0
    c2=0
    for a,b in zip(y_test,predictions):
        if(a==b):
            if(a==0):
                c1+=1
            else:
                c2+=1
    print([c1,c2]);
    print()
    print('Accuracy score: ', accuracy_score(y_test, predictions))
    print('Precision score: ', precision_score(y_test, predictions,average=None, labels=np.unique(y_test) ))
    print('Recall score: ', recall_score(y_test, predictions,average=None, labels=np.unique(y_test)))
    print('F1 score: ', f1_score(y_test, predictions,average=None, labels=np.unique(y_test)))

map_labels={"fraud":0,"bribery":1,"defamation":2,"corruption":3,"scam":4 ,"defaulter":5,"none":6}
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


for i in range(0,6):
    X=[]
    Y=[]
    for x,y in zip(list_articles,list_article_label):
        if(y!=6):
            if(y==i):
                X.append(x)
                Y.append(1)
            else:
                X.append(x)
                Y.append(0)
    train(X,Y)


#print('Accuracy score: ', accuracy_score(y_test, predictions))
#print('Precision score: ', precision_score(y_test, predictions,average=None, labels=np.unique(y_test) ))
#print('Recall score: ', recall_score(y_test, predictions,average=None, labels=np.unique(y_test)))
