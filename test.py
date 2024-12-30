import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, session
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import bs4 as bs
import urllib.request
import pickle
import requests
from datetime import date, datetime
import os
import json
import requests

filename = 'nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('tranform.pkl', 'rb'))


# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from bs4 import BeautifulSoup

print("Code started...")
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome()

imdb_id = "tt8178634"

# Open the IMDb reviews page
url = f'https://www.imdb.com/title/{imdb_id}/reviews?ref_=tt_ov_rt'
driver.get(url)

# Wait for the page to load fully
driver.implicitly_wait(5)

# Get the page source
html = driver.page_source

# Parse with BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
soup_result = soup.find_all("div", {"class": "ipc-html-content-inner-div"})

reviews_list = []  # list of reviews
reviews_status = []

for reviews in soup_result:
                if reviews.string:
                    reviews_list.append(reviews.string)
                    movie_review_list = np.array([reviews.string])
                    movie_vector = vectorizer.transform(movie_review_list)
                    pred = clf.predict(movie_vector)
                    reviews_status.append('Positive' if pred else 'Negative')

print(reviews_status)
# # Close the browser
driver.quit()    


#  if imdb_id != "":
#             # web scraping to get user reviews from IMDB site
#             options = webdriver.ChromeOptions()
#             options.add_argument('--headless')
#             driver = webdriver.Chrome()
#             print(imdb_id)
#             source = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
#             soup = bs.BeautifulSoup(source, 'lxml')
#             soup_result = soup.find_all("div", {"class": "ipc-html-content-inner-div"})

#             reviews_list = []  # list of reviews
#             reviews_status = []  # list of comments (good or bad)
#             for reviews in soup_result:
#                 if reviews.string:
#                     reviews_list.append(reviews.string)
#                     # passing the review to our model
#                     movie_review_list = np.array([reviews.string])
#                     movie_vector = vectorizer.transform(movie_review_list)
#                     pred = clf.predict(movie_vector)
#                     reviews_status.append('Positive' if pred else 'Negative')