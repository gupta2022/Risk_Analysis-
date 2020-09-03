#!/usr/bin/python
import pandas as pd
from pandas import DataFrame 
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

####################################################################################
####################################################################################
############################# Reading of Excel File ################################
####################################################################################
####################################################################################
df = pd.read_excel (r'Datasets/Data1.xlsx')
#paste the file address in between the quotes
#print (df)
CompanyName=[]
CompanyName=list(df['Company Name'])
#print(CompanyName)
A=[]
#A contains the list of Management Evaluation
A=list(df['Management Evaluation'])
B=[]
#B contains the list of Operational Assessment
B=list(df['Operational Assessment'])
C=[]
#C contains the list of Financial Assessment
C=list(df['Financial Assessment'])
D=[]
#D contains the list of Legal/Compliance Screening
D=list(df['Legal/Compliance Screening'])
Total=[]
#Total has the sub-total 
Total =list(df['Sub-Total'])
RiskBand=[]
RiskBand=list(df['Risk Band'])


#print(RiskBand)

Data ={'a':A,'b':B,'c':C,'d':D}
dt=DataFrame(Data,columns=['a','b','c','d'])
#print(dt)

####################################################################################
####################################################################################
############################## K-MEANS AND PLOTING #################################
####################################################################################
####################################################################################

kmeans = KMeans(n_clusters=4).fit(dt)
centroids = kmeans.cluster_centers_
print(centroids)

plt.scatter(dt['a'], dt['b'],dt['c'], dt['d'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()
