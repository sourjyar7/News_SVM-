# News_SVM-
A flask app that uses a SVM classifier to identify actual news articles from fake news,news sattires,etc.
This repository contains my first NLP project with python. I have attempted to train a Support Vector Machine classifier to recognise real news 
articles from fake ones or news sattires.

## Dataset Used

The dataset used can be found in a csv file 'train_data.csv' . I used BeautifulSoup api to scrape news articles from some popular news websites 
like the ANI,QUINT,etc and news sattires from websites like Scroll,FakingNews,etc and labelled them as 0 for genuine news and 1 for not news

## File Guide

The notebook 'Fake_news_detector.ipynb' contains the code for training the model and saves it in a 'model.pkl' file after training.
The 'Fake_api.py' contains the Flask code for deploying the model.
The templates folder contains an 'index.html' file which renders a basic html enabling us to test the model with new input.
