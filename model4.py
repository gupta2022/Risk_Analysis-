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
#there are 2 model that were trained to identify the keys because the keys scam and fraud were too iterlinked to be correctely indentified in the same model
filename="model2.pkl"

QUOTES = re.compile(r'(writes in|writes:|wrote:|says:|said:|^In article|^Quoted from|^\||^>)')

try:
    #loading the pickle file
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



X_train, X_test, y_train, y_test = train_test_split(data['article'], data['label'], test_size=0.2, random_state=1,shuffle=True)


cv = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True, stop_words='english')
X_train_cv = cv.fit_transform(X_train)
X_test_cv = cv.transform(X_test)

naive_bayes = MultinomialNB()
naive_bayes.fit(X_train_cv, y_train)
predictions = naive_bayes.predict(X_test_cv)
predictions_prob = naive_bayes.predict_proba(X_test_cv)
print(predictions)
print(predictions_prob)

pickle.dump(naive_bayes, open(filename, 'wb'))
pickle.dump(cv, open(filename.replace(".pkl","")+"cv.pkl", 'wb'))
print('Accuracy score: ', accuracy_score(y_test, predictions))
print('Precision score: ', precision_score(y_test, predictions,average='micro'))
print('Recall score: ', recall_score(y_test, predictions,average='micro'))
print('F1 score: ', f1_score(y_test, predictions,average='micro', labels=np.unique(y_test)))
