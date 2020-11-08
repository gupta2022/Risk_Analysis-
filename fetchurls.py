import glob
import pickle
import re
import requests
from bs4 import BeautifulSoup
import pandas

colnames = ['urls', 'tag','article']
data = pandas.read_csv('urlSet.csv')
print(data)
print(data.columns)
#list_articles=[]
#list_article_label=[]
#urls=data.urls.tolist()
#list1=data.tag.tolist()
c=data.count()

len1=c['article']
print(len1)
#print(urls)
#print(list1)

for index,row in data.iterrows():
    x=row['url']
    y=row['tag']
    if(len1<0):
        try:
            print(x)
            html_text = requests.get(x,timeout=10).text
            soup = BeautifulSoup(html_text, 'html.parser')
            #print(soup.get_text())
            data['article'][index]=soup.get_text()
            data.to_csv('urlSet.csv', index=False )
            #list_articles.append(soup.get_text())
            #list_article_label.append(y)
        except:
            print("Error")
    else:
        len1-=1

#with open("articles.txt", "wb") as fp:   #Pickling
#  pickle.dump(list_articles, fp)

#with open("articles_labels.txt", "wb") as fp:   #Pickling
#  pickle.dump(list_article_label, fp)
