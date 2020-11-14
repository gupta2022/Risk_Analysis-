import pickle
import nltk.stem
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd
import string
import re
from sklearn.naive_bayes import GaussianNB
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
def train(index):
    X_train, X_test, y_train, y_test = train_test_split(data['article'], data['label'], test_size=0.2, random_state=1,shuffle=True)
    for n, i in enumerate(y_train):
        if n==index:
            y_train[i]=1
        else:
            y_train[i]=0
    for n, i in enumerate(y_test):
        if n==index:
            y_test[i]=1
        else:
            y_test[i]=0
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

def preprocess_data(data):
    # Create a stemmer/lemmatizer
    stemmer = nltk.stem.SnowballStemmer('english')
    #lemmer = nltk.stem.WordNetLemmatizer()
    #for i in range(len(data)):
    # Remove header
    _, _, data = data.partition('\n\n')
    # Remove footer
    #lines = data.strip().split('\n')
    #for line_num in range(len(lines) - 1, -1, -1):
    #    line = lines[line_num]
    #    if line.strip().strip('-') == '':
    #        break
    #if line_num > 0:
    #    data = '\n'.join(lines[:line_num])
    # Remove quotes
    #data = '\n'.join([line for line in data.split('\n') if not QUOTES.search(line)])
    # Remove punctation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
    data = data.translate(str.maketrans('', '', string.punctuation))
    # Remove digits
    data = re.sub('\d', '', data)
    # Stem words
    data = ' '.join([stemmer.stem(word) for word in data.split()])
    #data = ' '.join([lemmer.lemmatize(word) for word in data.split()])
    # Return data
    return data


for index,row in data.iterrows():
    row = row.copy()
    data.loc[index,'article']=preprocess_data(row['article'])


for i in range(0,5):
    train(i)
