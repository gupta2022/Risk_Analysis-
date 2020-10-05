import glob
import pickle
import extract_msg
import re
import requests
from bs4 import BeautifulSoup

msgLocation="/home/aditya/Documents/ML Stuff/usefull/*.msg"


list_labels=["fraud","bribery","defamation","corruption","criminal","scam" ,"defaulter "]
list_articles=[]
list_article_label=[]


try:
    with open("articles.txt", "rb") as fp:   # Unpickling
        list_articles = pickle.load(fp)
    with open("articles_labels.txt", "rb") as fp:   # Unpickling
        list_article_label = pickle.load(fp)
except :
    print("No file detected")

files=glob.glob(msgLocation)
for fl in files:
    print (fl)
    label=""
    name=str(fl).lower()
    for x in list_labels:
        z= re.search(x, name)
        if z:
            label=x
            break

    f= r'%s' % fl
    msg = extract_msg.Message(f)
    msg_message = msg.body

    urls = re.findall('(?<=\<)(.*?)(?=\>)', msg_message)
    for url in urls:
        #print(url)
        try:
            z= re.search('source=alertsmail', url)
            if z ==None :
                furl=re.findall('=(?<=url=)(.*?)&ct', url)
                if furl:

                    print(furl[0])
                    html_text = requests.get(furl[0]).text
                    soup = BeautifulSoup(html_text, 'html.parser')
                    #print(soup.get_text())
                    list_articles.append(soup.get_text())
                    list_article_label.append(label)

                    print()
                    print()
        except :
            print("Error")
with open("articles.txt", "wb") as fp:   #Pickling
    pickle.dump(list_articles, fp)

with open("articles_labels.txt", "wb") as fp:   #Pickling
    pickle.dump(list_article_label, fp)
