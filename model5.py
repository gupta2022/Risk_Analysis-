import pickle
import nltk.stem
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd
#from sklearn.cluster import KMeans
import numpy as np

map_labels={"fraud":0,"bribery":1,"defamation":2,"corruption":3,"scam":4}
try:
    data = pd.read_pickle('dataset.pkl')
except:
    print("dataset Not found")

data['label'] = LabelEncoder().fit_transform(data['tag'])
#print(data)
data=data[['article','label']]
print(data)
data.article=data.article.astype(str)
X_train, X_test, y_train, y_test = train_test_split(data['article'], data['label'], test_size=0.2, random_state=1,shuffle=True )
