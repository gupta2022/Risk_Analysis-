
urls=[]
list1=[]
try:
    with open("articles.txt", "rb") as fp:   # Unpickling
        list_articles = pickle.load(fp)
    with open("articles_labels.txt", "rb") as fp:   # Unpickling
        list_article_label = pickle.load(fp)
except :
    print("No file detected")
for x,y in zip(urls,list1):
  html_text = requests.get(x).text
  soup = BeautifulSoup(html_text, 'html.parser')
  #print(soup.get_text())
  print([label,soup.get_text()])
  list_articles.append(soup.get_text())
  list_article_label.append(y)
with open("articles.txt", "wb") as fp:   #Pickling
  pickle.dump(list_articles, fp)

with open("articles_labels.txt", "wb") as fp:   #Pickling
  pickle.dump(list_article_label, fp)
