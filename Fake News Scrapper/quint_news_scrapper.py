import requests
import pandas as pd
from bs4 import BeautifulSoup
parent_url="https://www.thequint.com/news/"

categories=["world","india","business","education","politics","environment"]
dataset=[]


def explore(url):
    links=[]
    r=requests.get(url)
    page=r.content
    soup = BeautifulSoup(page, 'html5lib')
    news=soup.find_all('div',class_='card-elements story-card-block ctg-news')
    for n in news:
        links.append("https://www.thequint.com/"+n.find('a')['href'])
    return links    
    
def extract_data(links):
    for link in links:
        dict={}
        r=requests.get(link)
        page=r.content
        soup=BeautifulSoup(page,'html5lib')
        heads=soup.find_all('div',class_='story-article__body__left__top__headline')
        head=""
        for h in heads:
            head=h.find('h1',class_='merriweathersans-bold').get_text()

        div=soup.find_all('div',class_='story-article__content__element--text')
        text=""
        for d in div:
            paras=d.find_all('p')
            for p in paras:
                text=text+p.get_text()

        
        dict["head"]=head
        dict["body"]=text
        dict["label"]=0
        df=pd.DataFrame(dict,index=[0])
        df.to_csv('train_data.csv',mode='a',header=False,index=False)
        


for category in categories:
    url=parent_url+category+"/"
    print("Exploring : "+url+"\n")
    links=explore(url)
    print("Found "+str(len(links))+" items\n")
    extract_data(links)
    











