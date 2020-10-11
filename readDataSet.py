import pickle
import csv
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))

print(tf.__version__)
list_articles=[]
list_article_label=[]
with open("articles.txt", "rb") as fp:   # Unpickling
    list_articles = pickle.load(fp)
with open("articles_labels.txt", "rb") as fp:   # Unpickling
    list_article_label = pickle.load(fp)

for x,y in zip(list_articles,list_article_label):
    print([y,x])
    print()
    print()
