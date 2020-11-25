import glob
import pickle
import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import cleanDataset

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0'}
len1 = -1
try:
    data = pd.read_pickle('dataset.pkl')
    len1=len(data)
except:
    print("dataset.pkl not found")
    exit()
try:
    data1 = pd.read_csv('urlSet.csv')
    exit()
except:
    print("urlSet.csv not found")
    exit()
try:
    data1=data1[["url","tag"]]
    data=data.append(data1, ignore_index = True)
except:
    print("Check column names in csv are url and tag")
    exit()

print(data)
print(data.columns)

try:
    with open("index.txt", "rb") as fp:   # Unpickling
        len1 = pickle.load(fp)
except:
    print("1st run")

print(len1)
print(data.loc[len1+1])

for index, row in data.iterrows():
    row = row.copy()
    x = row['url']
    y = row['tag'].lower()
    if(index > len1):
        while True:
            flag = True
            try:
                time.sleep(0.01)
                html_text = requests.get(x, headers=headers, timeout=20).text
                soup = BeautifulSoup(html_text, 'html.parser')
                text = soup.get_text()
                data.loc[index, 'article'] = text
                data.loc[index, 'tag'] = y
                data.to_pickle('dataset.pkl')
                with open("index.txt", "wb") as fp:
                    pickle.dump(index, fp)

            except requests.ConnectionError as e:
                print(
                    "OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                print(str(e))
                if 'Connection reset by peer' not in e:
                    time.sleep(30)
                    flag = False
            except requests.Timeout as e:
                print("OOPS!! Timeout Error")
                print(str(e))
                flag = False
                time.sleep(20)
            except requests.RequestException as e:
                print("OOPS!! General Error")
                print(str(e))
            except Exception as e:
                print(e)
            finally:
                if flag:
                    break
clean()