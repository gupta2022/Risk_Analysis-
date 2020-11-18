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
#from sklearn.cluster import KMeans
import numpy as np
filename="model2.pkl"

QUOTES = re.compile(r'(writes in|writes:|wrote:|says:|said:|^In article|^Quoted from|^\||^>)')

try:
    data = pd.read_pickle('cleanDataset.pkl')
except:
    print("dataset Not found")

data['label'] = LabelEncoder().fit_transform(data['tag'])
#print(data)
data=data[['article','label']]
print(data)
## Full Model F1 score:  0.691239827668741

if( filename=="model1.pkl"):
    data=data[data['label']!=5] ##Model2 F1 score:  0.8933074684772065
    data=data[data['label']!=0]
    data=data[data['label']!=2]
else:
    data=data[data['label']!=3] ## Model1 F1 score:  0.8902527075812274
    data=data[data['label']!=1]

print(data)
data.article=data.article.astype(str)

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

#for index,row in data.iterrows():
#    row = row.copy()
#    data.loc[index,'article']=preprocess_data(row['article'])
#print(data)

X_train, X_test, y_train, y_test = train_test_split(data['article'], data['label'], test_size=0.2, random_state=1,shuffle=True)
#print(y_train.value_counts())
#print(y_test.value_counts())

#TODO try different tokeniizers
cv = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True, stop_words='english')
X_train_cv = cv.fit_transform(X_train)
X_test_cv = cv.transform(X_test)

naive_bayes = MultinomialNB()
naive_bayes.fit(X_train_cv, y_train)
predictions = naive_bayes.predict(X_test_cv)
predictions_prob = naive_bayes.predict_proba(X_test_cv)
print(predictions)
print(predictions_prob)
#for x in predictions_prob:
#    if 1.00000000e+00 not in x:
#        print(x)
pickle.dump(naive_bayes, open(filename, 'wb'))
print('Accuracy score: ', accuracy_score(y_test, predictions))
print('Precision score: ', precision_score(y_test, predictions,average='micro'))
print('Recall score: ', recall_score(y_test, predictions,average='micro'))
print('F1 score: ', f1_score(y_test, predictions,average='micro', labels=np.unique(y_test)))
