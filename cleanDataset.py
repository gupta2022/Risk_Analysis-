import pickle
import pandas as pd
import re

errorList=["page not found","error 40","error 50", "are you a robot","the connection was interrupted",
"the connection was reset","the connection has timed out","warning: potential security risk ahead",
"secure connection failed","did not connect: potential security issue","did not connect",
"unable to find the proxy server","the proxy server is refusing connections","unable to connect"]
try:
    data = pd.read_pickle('dataset.pkl')
    data=data[['url','tag','article']]
except:
    print("Error")


def hasError(x):
    for error in errorList:
        if error in x:
            return True


#print(data["article"].isnull().sum())
data=data.dropna()
print(data)
#df.drop(index, inplace = True)
count=0
for index,row in data.iterrows():
    row = row.copy()
    x=re.sub(r'\n\s*\n', '\n',row['article'] ).lower()
    #x=row['article'].replace('\n\n','\n').lower()
    if hasError(x):
        data.drop(index, inplace = True)
        #print(x)
        count+=1
print(data)
data.to_pickle('cleanDataset.pkl')
print(count)
