import pickle
import pandas as pd
import re

def clean():
    #ErrorList contains the list of expected errors for the scrapper
    errorList=["page not found","error 40","error 50", "are you a robot","the connection was interrupted",
    "the connection was reset","the connection has timed out","warning: potential security risk ahead",
    "secure connection failed","did not connect: potential security issue","did not connect",
    "unable to find the proxy server","the proxy server is refusing connections","unable to connect"]
    try:
        data = pd.read_pickle('dataset.pkl')
        data=data[['url','tag','article']]
    except:
        print("Error")

    #hasError checks if an error has occured and article was not feteched 
    def hasError(x):
        for error in errorList:
            if error in x:
                return True


    
    data=data.dropna()
    print(data)
    
    count=0
    #iterates the articles to find if an error had occurred 
    for index,row in data.iterrows():
        row = row.copy()
        x=re.sub(r'\n\s*\n', '\n',row['article'] ).lower()
        
        if hasError(x):
            data.drop(index, inplace = True)
            
            count+=1
    #print(data)
    data.to_pickle('cleanDataset.pkl')
    #print(count)