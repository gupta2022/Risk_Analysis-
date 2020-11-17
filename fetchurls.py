import glob
import pickle
import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0'}
try:
    data = pd.read_pickle('dataset.pkl')
    #noneData=pd.read_json("News_Category_Dataset_v2.json", lines=True)
    #noneData=noneData[['category','link','short_description']]
    #noneData=noneData.rename(columns={ "category":"tag", "link":"url"})
    #data=data.append(noneData, ignore_index = True)


except:
    print("Here")
    data = pd.read_csv('urlSet.csv')

print(data)
print(data.columns)
len1=-1
try:
    with open("index.txt", "rb") as fp:   # Unpickling
        len1 = pickle.load(fp)
except:
    print("1st run")
aCount=0
print(len1)
print(data.loc[len1+1])

for index,row in data.iterrows():
    row = row.copy()
    x=row['url']
    y=row['tag'].lower()
    if(index>len1 and aCount<100):
        while True:
            flag=True
            try:
                if ('crime' not in y and 'politics' not in y):
                    if ( 'fraud' not in row['short_description'] and 'bribe' not in row['short_description'] and 'scam' not in row['short_description'] and 'defame' not in row['short_description'] and 'corrupt' not in row['short_description']):
                        print(aCount,x,y)
                        time.sleep(0.01)
                        html_text = requests.get(x,headers=headers,timeout=20).text
                        soup = BeautifulSoup(html_text, 'html.parser')
                        text=soup.get_text()
                        data.loc[index,'article']=text
                        data.loc[index,'tag']='none'
                        #data.loc['article'][index]=soup.get_text()
                        data.to_pickle('dataset.pkl')
                        aCount+=1
                        with open("index.txt", "wb") as fp:
                            pickle.dump(index, fp)

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
