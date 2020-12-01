import pickle
import nltk.stem
import re
import string
import time # for timing script
import xml.etree.ElementTree as ET # built in library
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import requests
import sys
import threading
import os
from fake_useragent import UserAgent
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)
ua = UserAgent()

map_labels={0:"bribery",1:"corruption",2:"defamation",3:"fraud",4:"none",5:"scam"}
#used to identify a system
resultDataset=pd.DataFrame(columns=["company","bribery","corruption","defamation","fraud","scam","none"])
dateTime=str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")).replace("/","-")
dateTime=dateTime.replace(":","-")
headers = {
    'user-agent': ua.chrome }

def clean_url(searched_item,data_filter):
    x=datetime.now()
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


#geting the news from the searched query
def get_news(search_term, data_filter=None):
    url = clean_url(search_term, data_filter)
    response = requests.get(url)
    root= ET.fromstring(response.text)
    link = [i.text for i in root.findall('.//channel/item/link') ]

    return link
#genrating predictions using saved model
def getPredictions(company):

    companyData=pd.DataFrame( columns=( 'url', 'label') )
    j=0
    list_of_topics=["bribery","corruption","defamation","fraud","scam"]
    for search_term in list_of_topics:
        urlData = get_news(search_term+" "+company, data_filter="this year")
        for url in urlData:
            print(company,url)
            while True:
                flag=True
                try:
                    #dict={}
                    rowList=[]
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

                    if(p1[0]==4):
                        #dict["label"]=map_labels[p2]
                        rowList.append(map_labels[p2[0]])
                        companyData.loc[len(companyData.index)]=rowList
                    elif(p2[0]==4):
                        #dict["label"]=map_labels[p1]
                        rowList.append(map_labels[p1[0]])
                        companyData.loc[len(companyData.index)]=rowList
                    else:
                        #dict["label"]=map_labels[4]
                        rowList1=[ company,url,map_labels[p2[0]]  ]
                        rowList.append(map_labels[p1[0]])
                        companyData.loc[len(companyData.index)]=rowList
                        companyData.loc[len(companyData.index)]=rowList

                    #temp=pd.DataFrame.from_dict(dict)
                     #index=[len(resultDataset.index)],

                    #print(companyData)
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

#    companyData.to_csv(dateTime+"/companyData/"+company+".csv")
    companyData.to_sql(company, con=engine)

    dict1={"company":company}
    total=0
    for topic in list_of_topics:
        tempData = companyData[companyData["label"]==topic]
        dict1[topic] = len(tempData)
        total+=dict1[topic]
    dict1["none"]=len(companyData)-total
    resultDataset.loc[len(resultDataset.index)]=dict1
    #resultDataset.to_csv(dateTime+"/resultDataset.csv")

