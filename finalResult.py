import pickle
import nltk.stem
import re
import string
import time # for timing script
import xml.etree.ElementTree as ET # built in library
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import requests
import sys


#For help only
map_labels={0:"bribery",1:"corruption",2:"defamation",3:"fraud",4:"none",5:"scam"}
cv = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True, stop_words='english')


resultDataset=pd.DataFrame()

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filePath = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filePath)
data = pd.read_csv(filePath)

def clean_url(searched_item,data_filter):
    x =pd.datetime.today()
    today =str(x)[:10]
    yesterday = str(x + pd.Timedelta(days=-1))[:10]
    this_week = str(x + pd.Timedelta(days=-7))[:10]
    if data_filter == 'today':
        time = 'after%3A' + yesterday
    elif data_filter == 'this_week':
        time = 'after%3A'+ this_week + '+before%3A' + today
    elif data_filter == 'this_year':
        time = 'after%3A'+str(x.year -1)
    elif str(data_filter).isdigit():
        temp_time2= str(x + pd.Timedelta(days=-int(data_filter)))[:10]
        temp_time = str(x + pd.Timedelta(days=-int(data_filter)-90))[:10]
        print (temp_time)
        time =  'after%3A'+ temp_time + '+before%3A' + temp_time2
    else:
        time=''
    url = f'https://news.google.com/rss/search?q={searched_item}+'+time+'&hl=en-US&gl=US&ceid=US%3Aen'
    print (url)
    return url

# clear the description


def get_news(search_term, data_filter=None):
    url = clean_url(search_term, data_filter)
    response = requests.get(url)
    root= ET.fromstring(response.text)
    link = [i.text for i in root.findall('.//channel/item/link') ]

    return link

companyList=data["company"].tolist()

try:
    model1 = pickle.load(open("model1.pkl", 'rb'))
    model2 = pickle.load(open("model2.pkl", 'rb'))
except:
    print("Train The models First or courupt models")
    exit()

def getPredictions(company):

    list_of_topics=["bribery","corruption","defamation","fraud","scam"]
    for search_term in list_of_topics:
        urlData = get_news(search_term+" "+company, data_filter="this year")
        for url in urlData:
            dict={}
            dict["company"]=company
            dict["url"]=url
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'html.parser')
            articles=[]
            articles.append(soup.get_text())
            X_train_cv = cv.fit_transform(articles)
            p1 = model1.predict(X_test_cv)
            p2 = model2.predict(X_test_cv)
            if(p1==4):
                dict["label"=map_labels[p2]
            elif(p2==4):
                dict["label"=map_labels[p1]
            else:
                dict["label"=map_labels[4]

            temp=pd.DataFrame(dict)
            resultDataset.append(temp,ignore_index = True)



for company in companyList:
    getPredictions( getArticles(company) )
resultDataset.to_csv("resultDataset.csv")
