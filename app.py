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
import mysql.connector
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from bs4 import BeautifulSoup

# load the nlp model and tfidf vectorizer from disk
filename = 'nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('tranform.pkl', 'rb'))


# converting list of string to list (eg. "["abc","def"]" to ["abc","def"])
def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["', '')
    my_list[-1] = my_list[-1].replace('"]', '')
    return my_list


# convert list of numbers to list (eg. "[1,2,3]" to [1,2,3])
def convert_to_list_num(my_list):
    my_list = my_list.split(',')
    my_list[0] = my_list[0].replace("[", "")
    my_list[-1] = my_list[-1].replace("]", "")
    return my_list


def get_suggestions():
    data = pd.read_csv('main_data.csv')
    return list(data['movie_title'].str.capitalize())


app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = mysql.connector.connect(host="localhost", user="root", password="", database="cinemamovie")
curser = conn.cursor()


@app.route("/")
def login():
    return render_template('login.html')


@app.route("/home-marvel")
def home():
    if 'user_id' in session:
        suggestions = get_suggestions()
        name=session.get("name")
        
        return render_template('home.html', suggestions=suggestions,username=name)
    else:
        return redirect('/')
    

@app.route("/home-barbie")
def home1():
    if 'user_id' in session:
        suggestions = get_suggestions()
        name=session.get("name")
        
        return render_template('home1.html', suggestions=suggestions,username=name)
    else:
        return redirect('/')


@app.route("/404")
def lostpage():
    return render_template('blackbox.html')


@app.route('/login_validation', methods=['POST', 'GET'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    curser.execute(""" SELECT * FROM `user` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email,
                                                                                                        password))
    users = curser.fetchall()
    
    if len(users) > 0:
        session['user_id'] = users[0][0]
        session["name"]=users[0][1]
        return redirect('/home-marvel')
    else:
        return redirect('/404')


@app.route('/add_user', methods=['POST'])
def add_user():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')

    curser.execute(""" INSERT INTO `user` (`user_id`,`user_name`,`email`,`password`) 
                    VALUES(NULL,'{}','{}','{}') """.format(user_name, email, password))
    conn.commit()
    return redirect('/')


@app.route("/populate-matches", methods=["POST"])
def populate_matches():

    if 'user_id' in session:
        # getting data from AJAX request
        res = json.loads(request.get_data("data"))
        movies_list = res['movies_list']

        movie_cards = {"https://image.tmdb.org/t/p/original" + movies_list[i]['poster_path']
                       if movies_list[i]['poster_path'] else "/static/movie_placeholder.jpeg": [movies_list[i]['title'],
                                                                                                movies_list[i][
                                                                                                    'original_title'],
                                                                                                movies_list[i][
                                                                                                    'vote_average'],
                                                                                                datetime.strptime(
                                                                                                    movies_list[i][
                                                                                                        'release_date'],
                                                                                                    '%Y-%m-%d').year if
                                                                                                movies_list[i][
                                                                                                    'release_date'] else "N/A",
                                                                                                movies_list[i]['id']] for i
                       in range(len(movies_list))}
        return render_template('recommend.html', movie_cards=movie_cards)
    else:
        return redirect('/')


@app.route("/recommend", methods=["POST"])
def recommend():

    if 'user_id' in session:
        # getting data from AJAX request
        title = request.form['title']
        cast_ids = request.form['cast_ids']
        cast_names = request.form['cast_names']
        cast_chars = request.form['cast_chars']
        cast_bdays = request.form['cast_bdays']
        cast_bios = request.form['cast_bios']
        cast_places = request.form['cast_places']
        cast_profiles = request.form['cast_profiles']
        imdb_id = request.form['imdb_id']
        poster = request.form['poster']
        genres = request.form['genres']
        overview = request.form['overview']
        vote_average = request.form['rating']
        vote_count = request.form['vote_count']
        rel_date = request.form['rel_date']
        release_date = request.form['release_date']
        runtime = request.form['runtime']
        status = request.form['status']
        rec_movies = request.form['rec_movies']
        rec_posters = request.form['rec_posters']
        rec_movies_org = request.form['rec_movies_org']
        rec_year = request.form['rec_year']
        rec_vote = request.form['rec_vote']
        rec_ids = request.form['rec_ids']

        # get movie suggestions for auto complete
        suggestions = get_suggestions()

        # call the convert_to_list function for every string that needs to be converted to list
        rec_movies_org = convert_to_list(rec_movies_org)
        rec_movies = convert_to_list(rec_movies)
        rec_posters = convert_to_list(rec_posters)
        cast_names = convert_to_list(cast_names)
        cast_chars = convert_to_list(cast_chars)
        cast_profiles = convert_to_list(cast_profiles)
        cast_bdays = convert_to_list(cast_bdays)
        cast_bios = convert_to_list(cast_bios)
        cast_places = convert_to_list(cast_places)

        # convert string to list (eg. "[1,2,3]" to [1,2,3])
        cast_ids = convert_to_list_num(cast_ids)
        rec_vote = convert_to_list_num(rec_vote)
        rec_year = convert_to_list_num(rec_year)
        rec_ids = convert_to_list_num(rec_ids)

        # rendering the string to python string
        for i in range(len(cast_bios)):
            cast_bios[i] = cast_bios[i].replace(r'\n', '\n').replace(r'\"', '\"')

        for i in range(len(cast_chars)):
            cast_chars[i] = cast_chars[i].replace(r'\n', '\n').replace(r'\"', '\"')

            # combining multiple lists as a dictionary which can be passed to the html file so that it can be
            # processed easily and the order of information will be preserved
        movie_cards = {rec_posters[i]: [rec_movies[i], rec_movies_org[i], rec_vote[i], rec_year[i], rec_ids[i]] for i in
                       range(len(rec_posters))}

        casts = {cast_names[i]: [cast_ids[i], cast_chars[i], cast_profiles[i]] for i in range(len(cast_profiles))}

        cast_details = {cast_names[i]: [cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i]] for i in
                        range(len(cast_places))}

        if imdb_id != "":
            # web scraping to get user reviews from IMDB site
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome()
            url = f'https://www.imdb.com/title/{imdb_id}/reviews?ref_=tt_ov_rt'
            driver.get(url)
            # Wait for the page to load fully
            driver.implicitly_wait(5)
            # Get the page source
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            soup_result = soup.find_all("div", {"class": "ipc-html-content-inner-div"})

            reviews_list = []  # list of reviews
            reviews_status = []  # list of comments (good or bad)
            for reviews in soup_result:
                if reviews.string:
                    reviews_list.append(reviews.string)
                    # passing the review to our model
                    movie_review_list = np.array([reviews.string])
                    movie_vector = vectorizer.transform(movie_review_list)
                    pred = clf.predict(movie_vector)
                    reviews_status.append('Positive' if pred else 'Negative')
            driver.quit()   

            # getting current date
            movie_rel_date = ""
            curr_date = ""
            if rel_date:
                today = str(date.today())
                curr_date = datetime.strptime(today, '%Y-%m-%d')
                movie_rel_date = datetime.strptime(rel_date, '%Y-%m-%d')

            # combining reviews and comments into a dictionary
            movie_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}
        
            # passing all the data to the html file
            return render_template('recommend.html', title=title, poster=poster, overview=overview,
                                   vote_average=vote_average,
                                   vote_count=vote_count, release_date=release_date, movie_rel_date=movie_rel_date,
                                   curr_date=curr_date, runtime=runtime, status=status, genres=genres,
                                   movie_cards=movie_cards, reviews=movie_reviews, casts=casts, cast_details=cast_details)

        else:
            return render_template('recommend.html', title=title, poster=poster, overview=overview,
                                   vote_average=vote_average,
                                   vote_count=vote_count, release_date=release_date, movie_rel_date="", curr_date="",
                                   runtime=runtime, status=status, genres=genres, movie_cards=movie_cards, reviews="",
                                   casts=casts, cast_details=cast_details)
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)




