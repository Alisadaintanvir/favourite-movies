from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
import requests
from flask_migrate import Migrate
from db import db, Movie
from form import MovieForm, EditMovieForm, FindMovieForm
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
Bootstrap(app)

db.init_app(app)
migrate = Migrate(app, db)
session = db.session

TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_INFO_URL = "https://api.themoviedb.org/3/movie"
TMDB_IMAGE_URL = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")


@app.route("/")
def home():
    movies = Movie.query.order_by(Movie.ranking.desc()).all()
    return render_template("index.html", movies=movies)


@app.route('/add', methods=["GET", "POST"])
def add():
    form = FindMovieForm()
    if request.method == 'POST' and form.validate_on_submit():
        response = requests.get(TMDB_SEARCH_URL, params={"api_key": TMDB_API_KEY, "language": "en-US",
                                                         "query": form.title.data})
        data = response.json()['results']
        return render_template('select.html', options=data)

    return render_template('add.html', form=form)


@app.route('/find')
def find():
    movie_id = request.args.get('id')
    if movie_id:
        movie_api_url = f"{TMDB_INFO_URL}/{movie_id}"
        response = requests.get(movie_api_url, params={"api_key": TMDB_API_KEY, "language": "en-US"})
        data = response.json()
        print(data)
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split('-')[0],
            description=data["overview"],
            img_url=f"{TMDB_IMAGE_URL}/{data['poster_path']}"
        )
        session.add(new_movie)
        session.commit()
        return redirect(url_for('edit', id=new_movie.id))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    movie_id = request.args.get('id')
    movie_selected = session.get(Movie, movie_id)
    form = EditMovieForm(obj=movie_selected)

    if request.method == 'POST' and form.validate_on_submit():
        existing_movie = session.query(Movie).filter(Movie.ranking == form.ranking.data).first()
        if existing_movie and existing_movie != movie_selected:
            flash(f"A movie name {existing_movie.title} with the same ranking already exists. "
                  f"Please change the ranking.", 'error')
        else:
            movie_selected.ranking = form.ranking.data
            movie_selected.rating = form.rating.data
            movie_selected.review = form.review.data
            session.commit()
            return redirect(url_for('home'))
    return render_template('edit.html', form=form, movie=movie_selected)


@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = session.get(Movie, movie_id)
    if movie_to_delete:
        session.delete(movie_to_delete)
        session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
