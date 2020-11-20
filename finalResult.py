import pickle
import nltk.stem
import re
import string
import time # for timing script
import xml.etree.ElementTree as ET # built in library
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import requests
import sys


#For help only
map_labels={0:"bribery",1:"corruption",2:"defamation",3:"fraud",4:"none",5:"scam"}
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0' }
cv = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True, stop_words='english')

try:
    resultDataset = pd.read_csv('resultDataset.csv')

except:
    print("First run")
    resultDataset=pd.DataFrame( columns=('company', 'url', 'label') )

try:
    with open("index.txt", "rb") as fp:   # Unpickling
        len1 = pickle.load(fp)
except:
    print("1st run")


Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filePath = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filePath)
data = pd.read_csv(filePath)

def clean_url(searched_item,data_filter):
    x=pd.datetime.today()
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
    cv1=pickle.load(open("model1cv.pkl", 'rb'))
    cv2=pickle.load(open("model2cv.pkl", 'rb'))
except:
    print("Train The models First or courupt models")
    exit()

def getPredictions(company):

    list_of_topics=["bribery","corruption","defamation","fraud","scam"]
    for search_term in list_of_topics:
        list_of_topics[1]
        urlData = get_news(search_term+" "+company, data_filter="this year")
        for url in urlData:
            while True:
                flag=True
                try:
                    #dict={}
                    rowList=[]
                    rowList.append(company)
                    #dict["company"]=company
                    #dict["url"]=url
                    rowList.append(url)
                    time.sleep(0.01)
                    html_text = requests.get(url,headers=headers,timeout=20).text
                    soup = BeautifulSoup(html_text, 'html.parser')
                    articles=[]
                    articles.append(soup.get_text())
                    X_test_cv1 = cv1.transform(articles)
                    X_test_cv2 = cv2.transform(articles)
                    p1 = model1.predict(X_test_cv1)
                    p2 = model2.predict(X_test_cv2)

                    if(p1==4):
                        #dict["label"]=map_labels[p2]
                        rowList.append(map_labels[p2])
                    elif(p2==4):
                        #dict["label"]=map_labels[p1]
                        rowList.append(map_labels[p1])
                    else:
                        #dict["label"]=map_labels[4]
                        rowList.append(map_labels[4])

                    #temp=pd.DataFrame.from_dict(dict)
                    resultDataset.loc[len(resultDataset.index)]=rowList #index=[len(resultDataset.index)],

                    print(resultDataset)
                    #resultDataset=resultDataset.append(temp,ignore_index = True, verify_integrity=False, sort=None)

                except requests.ConnectionError as e:

                    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                    print(str(e))
                    if 'Connection reset by peer' not in e:
                        time.sleep(30)
                        flag=False

                except requests.Timeout as e:

                    print("OOPS!! Timeout Error")
                    print(str(e))
                    flag=False
                    time.sleep(20)

                except requests.RequestException as e:

                    print("OOPS!! General Error")
                    print(str(e))

                except Exception as e:

                    print(e)

                finally:
                    if flag:
                        break



for company in companyList:
    #company
    getPredictions( company )
    resultDataset.to_csv("resultDataset.csv")
