import pickle
list_articles=[]
list_article_label=[]
with open("articles.txt", "rb") as fp:   # Unpickling
    list_articles = pickle.load(fp)
with open("articles_labels.txt", "rb") as fp:   # Unpickling
    list_article_label = pickle.load(fp)

for x,y in zip(list_articles,list_article_label):
    print([y,x])
    print()
    print()
