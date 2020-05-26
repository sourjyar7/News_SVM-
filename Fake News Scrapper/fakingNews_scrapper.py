import requests
import pandas as pd
from bs4 import BeautifulSoup
parent_url="http://www.fakingnews.com/"
categories=["india","world","sports","business","society","entertainment","politics","social-media","technology","snippets","media"]
dataset=[]



def explore(url):
    links=[]
    r=requests.get(url)
    page=r.content
    soup = BeautifulSoup(page, 'html5lib')
    links.append(parent_url+soup.find('h1',class_='category-story-title clear').find('a')['href'])
    news=soup.find_all('div',class_='story-box')
    for n in news:
        links.append(parent_url+n.find('a')['href'])
    return links    
    
def extract_data(links):
    for link in links:
        dict={}
        text=""
        r=requests.get(link)
        page=r.content
        soup=BeautifulSoup(page,'html5lib')
        head=soup.find('h1').get_text()
        body=soup.find('div',class_='article-content').find_all('p')
        dict["head"]=head
        for p in body:
            text=text+p.get_text()

        dict["body"]=text
        dict["label"]=1
        df=pd.DataFrame(dict,index=[0])
        df.to_csv('train_data.csv',mode='a',header=False,index=False)
       


for category in categories:
    url=parent_url+"/category/"+category+"/"
    print("Exploring : "+url+"\n")
    links=explore(url)
    print("Found "+str(len(links))+" items\n")
    extract_data(links)
    


