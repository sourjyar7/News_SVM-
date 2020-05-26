from flask import Flask, render_template, request, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
import string, codecs, re, nltk, pickle
import numpy as np
import pandas as pd
app=Flask(__name__)

#routes
@app.route('/')
def func():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def handler():
    text=request.form['news']
    inp=preprocess(text)
    model=pickle.load(open('fake_svm.pkl','rb'))
    result=model.predict(inp.toarray())
    if result ==0:
        return render_template('index.html', value="It appears to be a genuine article !")
    else:
        return render_template('index.html', value="It seems to be a sattire !")    

def preprocess(x):
     df=pd.read_csv('train_data.csv')
     df.drop(df.iloc[:,3:],inplace=True,axis=1)
     df.drop_duplicates(subset="Head",inplace=True)
     df.dropna(inplace=True)
     df['Clean_Body']=df['Body'].apply(lambda x:remove_punct(x))
     df['Clean_Body']=df['Clean_Body'].apply(lambda x:sanitize(x))
     df['Clean_Body']=df['Clean_Body'].apply(lambda x:tokenize(x))
     df['Clean_Body']=df['Clean_Body'].apply(lambda x:lemmatize(x))
     tfidf_vect=TfidfVectorizer(analyzer=lemmatize)
     tfidf_vect.fit(df['Clean_Body'])
     d=pd.DataFrame({"body" : x},index=[0])
     d['Clean_Body']=d['body'].apply(lambda x:remove_punct(x))
     d['Clean_Body']=d['Clean_Body'].apply(lambda x:sanitize(x))
     d['Clean_Body']=d['Clean_Body'].apply(lambda x:tokenize(x))
     d['Clean_Body']=d['Clean_Body'].apply(lambda x:lemmatize(x)) 
     final=tfidf_vect.transform(d['Clean_Body'])
     return final


def remove_punct(str):
    if(type(str) != float):
        txt = "".join([c for c in str if c not in string.punctuation])
        return txt    
def detect_language(character):
    maxchar = max(character)
    if u'\u0900' <= maxchar <= u'\u097f':
        return False
    else:
        return True

    
def sanitize(text):
    text=str(text)
    para ="".join([c for c in text if (detect_language(c))])
    return para


def tokenize(text):
    text=str(text)
    tokens=re.split('\W+',text)
    return tokens


wnl=nltk.WordNetLemmatizer()
def lemmatize(words):
    word=[wnl.lemmatize(word) for word in words]
    return word


if __name__=='__main__':
    app.run(debug=True)
