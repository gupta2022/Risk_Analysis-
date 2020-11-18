import pickle
import nltk.stem
import re
import string
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score,f1_score
import pandas as pd
import numpy as np

#For help only
map_labels={"bribery":0,"corruption":1,"defamation":2,"fraud":3,"none":4,"scam":5}
cv = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True, stop_words='english')
try:
    model1 = pickle.load(open("model1.pkl", 'rb'))
    model2 = pickle.load(open("model2.pkl", 'rb'))
except:
    print("Train The models First or courupt models")
#TODO get X_train
def getPredictions():
    X_train_cv = cv.fit_transform(X_train)
    prediction1 = model1.predict(X_test_cv)
    prediction2 = model2.predict(X_test_cv)

    #TODO Store the results
