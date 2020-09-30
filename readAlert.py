import glob
import extract_msg
import re
import requests
from bs4 import BeautifulSoup


files=glob.glob("C:/Users/venig/Desktop/ML Stuff/ML Stuff/usefull/*.msg")
for fl in files:
    print (fl)
    #f = r'Google Alert - Bribery India (61).msg'  # Replace with yours
    f= r'%s' % fl
    msg = extract_msg.Message(f)
    msg_sender = msg.sender
    msg_date = msg.date
    msg_subj = msg.subject
    msg_message = msg.body



    #print('Body: {}'.format(msg_message))
    #for line in msg_message:
    #print(msg_message)
    urls = re.findall('(?<=\<)(.*?)(?=\>)', msg_message)
    for url in urls:
        #print(url)
        z= re.search('source=alertsmail', url)
        if z ==None :
            furl=re.findall('=(?<=url=)(.*?)&ct', url)
            if furl:
                print(furl[0])
                html_text = requests.get(furl[0]).text
                soup = BeautifulSoup(html_text, 'html.parser')
                print(soup.get_text())
                print()
                print()
