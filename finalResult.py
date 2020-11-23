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
import tkinter.messagebox
import requests
import sys
import os


#For help only
map_labels={0:"bribery",1:"corruption",2:"defamation",3:"fraud",4:"none",5:"scam"}
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0' }


index=-1
filePath=""
answer=False

try:
    resultDataset = pd.read_csv('resultDataset.csv')

except:
    print("First run")
    resultDataset=pd.DataFrame(  )

try:
    with open("cindex.txt", "rb") as fp:   # Unpickling
        index = pickle.load(fp)
    with open("filepath.txt", "rb") as fp:   # Unpickling
        filePath = pickle.load(fp)
except:
    print("1st run")

if(filePath!=""):
    answer = messagebox.askokcancel("Resume", "Found and old instance, countinue that?")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
if(answer==False):
    filePath = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filePath)
if(filePath==()):
    messagebox.showinfo("Error","Connot Work Without CSV file")
    exit()
try:
    data = pd.read_csv(filePath)
except:
    messagebox.showinfo("Error","Unable Read The csv")
    exit()

try:
    companyList=data["company"].tolist()
except:
    messagebox.showinfo("Error","Check if CSV contains column named 'company'")
    exit()

with open("filePath.txt", "wb") as fp:
    pickle.dump(filePath, fp)
try:
    model1 = pickle.load(open("model1.pkl", 'rb'))
    model2 = pickle.load(open("model2.pkl", 'rb'))
    cv1=pickle.load(open("model1cv.pkl", 'rb'))
    cv2=pickle.load(open("model2cv.pkl", 'rb'))
except:
    messagebox.showinfo("Error","Train Models first")
    exit()


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



def get_news(search_term, data_filter=None):
    url = clean_url(search_term, data_filter)
    response = requests.get(url)
    root= ET.fromstring(response.text)
    link = [i.text for i in root.findall('.//channel/item/link') ]

    return link

def getPredictions(company):

    companyData=pd.DataFrame( columns=('company', 'url', 'label') )

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

    outdir = './companyData'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    companyData.to_csv("companyData/"+company+".csv")

    dict={"company":company}
    for topic in list_of_topics:
        companyData = companyData.apply(lambda x : True
                if x['label'] == topic else False, axis = 1)

        dict[topic] = len(companyData[companyData == True].index)
    resultDataset.loc[len(resultDataset.index)]=dict


for i,company in enumerate(companyList):
    print(i,index)
    if(i>index):
        print(index)
        getPredictions( company )
        resultDataset.to_csv("resultDataset.csv")
        with open("cindex.txt", "wb") as fp:
            pickle.dump(i, fp)
