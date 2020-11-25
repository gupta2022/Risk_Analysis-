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
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox
import requests
import sys
import threading
import os


#For help only
#tags searched
map_labels={0:"bribery",1:"corruption",2:"defamation",3:"fraud",4:"none",5:"scam"}
#used to identify a system
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0' }


index=-1 #used to resume progress
filePath=""
answer=False # answer for whether user wants to resume
dateTime=str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")).replace("/","-")
dateTime=dateTime.replace(":","-")
firstRun=True
resultDataset=pd.DataFrame(columns=["company","bribery","corruption","defamation","fraud","scam","none"])

try:
    with open("dtime.txt", "rb") as fp:   # Unpickling
        dateTime = pickle.load(fp)
        if(dateTime!=""):
            firstRun=False 
except:
    print("1st Run")
    dateTime=str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")).replace("/","-")
    dateTime=dateTime.replace(":","-")

if( firstRun==False):
    try:
        #reading the csv file containg url and tags
        resultDataset = pd.read_csv(dateTime+'/resultDataset.csv')
    except:       
        messagebox.showinfo("Error","ResultDataset.csv not found to reume operation")
        exit()

    try:
        #loading the index of the last known position
        with open(dateTime+"/cindex.txt", "rb") as fp:   # Unpickling
            index = pickle.load(fp)
    except:
        messagebox.showinfo("Error","index.txt not found to reume operation")
        exit()

    try:
        with open(dateTime+"/filepath.txt", "rb") as fp:   # Unpickling
            filePath = pickle.load(fp)
    except:
        messagebox.showinfo("Error","filepath.txt not found to reume operation")
        exit()
    #checking error for filepath
    if(filePath!=""):
        answer = messagebox.askokcancel("Resume", "Found and old instance, countinue that?")
    
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    
    if(answer==False):
        filePath = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        index=-1
        resultDataset=pd.DataFrame(columns=["company","bribery","corruption","defamation","fraud","scam","none"])
    

else:
    Tk().withdraw()
    filePath = askopenfilename()
#checking if not file has been selected
if(filePath==()):
    messagebox.showinfo("Error","Connot Work Without CSV file")
    exit()
try:
    data = pd.read_csv(filePath)
except:
    messagebox.showinfo("Error","Unable Read The csv")
    exit()

try:
    #reading the list of companies
    companyList=data["company"].tolist()
except:
    messagebox.showinfo("Error","Check if CSV contains column named 'company'")
    exit()
#saving date & time of current operation for resumming in future
with open("dtime.txt", "wb") as fp:
    pickle.dump(dateTime, fp)
outdir = './'+dateTime
if not os.path.exists(outdir):
    os.mkdir(outdir)
with open(dateTime+"/filePath.txt", "wb") as fp:
    pickle.dump(filePath, fp)
with open(dateTime+"/cindex.txt", "wb") as fp:
    pickle.dump(index, fp)
resultDataset.to_csv(dateTime+"/resultDataset.csv")
try:
    model1 = pickle.load(open("model1.pkl", 'rb'))
    model2 = pickle.load(open("model2.pkl", 'rb'))
    cv1=pickle.load(open("model1cv.pkl", 'rb'))
    cv2=pickle.load(open("model2cv.pkl", 'rb'))
except:
    messagebox.showinfo("Error","Train Models first")
    exit()

#generating the url for fetching of 100 articles for a topic
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

    companyData=pd.DataFrame( columns=('company', 'url', 'label') )
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
                    j+=1
                    print(j)
                    progress_bar['value'] = int( j/ 5)
                    label_4["text"]=" "+str(int(j/5))+"%"
                    master.update()


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

    outdir = './'+dateTime+'/companyData'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    companyData.to_csv(dateTime+"/companyData/"+company+".csv")

    dict1={"company":company}
    total=0
    for topic in list_of_topics:
        tempData = companyData[companyData["label"]==topic]
        dict1[topic] = len(tempData)
        total+=dict1[topic]
    dict1["none"]=len(companyData)-total
    resultDataset.loc[len(resultDataset.index)]=dict1


master = Tk()
 

# Create a progressbar widget
progress_bar = ttk.Progressbar(master, orient="horizontal",
                              mode="determinate", maximum=100, value=0)
 
# And a label for it
label_1 = Label(master, text="Companies Done:")
label_2 = Label(master, text="")
label_3 = Label(master, text="")
label_4 = Label(master, text="")
label_5 = Label(master, text="Currently Fetching For:")
label_6 = Label(master, text="Progress:")
 
# Use the grid manager
label_1.grid(row=0, column=0)
label_2.grid(row=1, column=1)
label_3.grid(row=0, column=1)
label_4.grid(row=2, column=2)
label_5.grid(row=1, column=0)
label_6.grid(row=2, column=0)
progress_bar.grid(row=2, column=1)
 
# Necessary, as the master object needs to draw the progressbar widget
# Otherwise, it will not be visible on the screen
master.update()
 
progress_bar['value'] = 0
master.update()

maxVal=len(companyList)
for i,company in enumerate(companyList):
    label_3["text"]=str(i)+"/"+str(maxVal)
    label_2["text"]=company
    print(i,index)
    if(i>index):
        print(index)
        getPredictions( company)
        resultDataset.to_csv(dateTime+"/resultDataset.csv")
        with open(dateTime+"/cindex.txt", "wb") as fp:
            pickle.dump(i, fp)
    progress_bar['value'] =0
    master.update()
with open("dtime.txt", "wb") as fp:
    pickle.dump("", fp)

with open(dateTime+"/filePath.txt", "wb") as fp:
    pickle.dump("", fp)
with open(dateTime+"/cindex.txt", "wb") as fp:
    pickle.dump(-1, fp)
exit()     
# The application mainloop
mainloop()