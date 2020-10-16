import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

#Loading the data set - training data.
from sklearn.datasets import fetch_20newsgroups




map_labels={"fraud":0,"bribery":1,"defamation":2,"corruption":3,"criminal":4,"scam":5 ,"defaulter":6}
list_articles=[]
list_article_label=[]
articles=[]


with open("articles.txt", "rb") as fp:   # Unpickling
    list_articles = pickle.load(fp)
with open("articles_labels.txt", "rb") as fp:   # Unpickling
    list_article_label = pickle.load(fp)
for i in range(0,len(list_article_label)):
    list_article_label[i]=map_labels[list_article_label[i]]

twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(list_articles)
X_train_counts.shape
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_train_tf.shape
clf = MultinomialNB().fit(X_train_tfidf, list_article_label)
