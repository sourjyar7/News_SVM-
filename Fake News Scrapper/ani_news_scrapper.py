import requests
import pandas as pd
from bs4 import BeautifulSoup
parent_url="https://aninews.in"
categories=["world","sports","business","lifestyle","health","science","tech","environment"]
dataset=[]


def explore(url):
    links=[]
    r=requests.get(url)
    page=r.content
    soup = BeautifulSoup(page, 'html5lib')
    links.append("https://aninews.in/"+soup.find('article').find('div',class_='content').find('a')['href'])
    news=soup.find_all('figcaption')
    for n in news:
        links.append("https://aninews.in/"+n.find('a')['href'])
    return links    
    
def extract_data(links):
    for link in links:
        dict={}
        r=requests.get(link)
        page=r.content
        soup=BeautifulSoup(page,'html5lib')
        head=soup.find('h1').get_text()
        text=soup.find('div',class_='content',itemprop='articleBody').find('p').get_text()
        dict["head"]=head
        dict["body"]=text
        dict["label"]=0
        df=pd.DataFrame(dict,index=[0])
        df.to_csv('train_data.csv',mode='a',header=False,index=False)
        


for category in categories:
    url=parent_url+"/category/"+category+"/"
    print("Exploring : "+url+"\n")
    links=explore(url)
    print("Found "+str(len(links))+" items\n")
    extract_data(links)
    


