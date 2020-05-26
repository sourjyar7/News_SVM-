import requests
import pandas as pd
from bs4 import BeautifulSoup
parent_url="https://scroll.in/"

dataset=[]

def explore(url):
    links=[]
    r=requests.get(url)
    page=r.content
    soup = BeautifulSoup(page, 'html5lib')
    links.append(soup.find('a',class_='story-gradient')['href'])
    news=soup.find_all('li',class_='row-story')
    for n in news:
        links.append(n.find('a')['href'])
    return links    
    
def extract_data(links):
    for link in links:
        dict={}
        text=""
        r=requests.get(link)
        page=r.content
        soup=BeautifulSoup(page,'html5lib')
        head=soup.find('h1').get_text()
        body=soup.find('div',class_='article-body',id='article-contents').find_all('p')
        dict["head"]=head
        for p in body:
            text=text+p.get_text()
        dict["body"]=text
        dict["label"]=1
        df=pd.DataFrame(dict,index=[0])
        df.to_csv('train_data.csv',mode='a',index=False,header=False)



url=parent_url
print("Exploring : "+url+"\n")
links=explore(url)
print("Found "+str(len(links))+" items\n")
extract_data(links)

