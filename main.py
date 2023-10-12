from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import requests
from flask_migrate import Migrate
from db import db, Movie
from form import MovieForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
Bootstrap(app)

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return render_template("index.html", movies=Movie.query.all())


@app.route('/add', methods=["GET", "POST"])
def add():
    form = MovieForm()
    if request.method == 'POST':
        new_movie = Movie(
            title=form.title.data,
            year=form.year.data,
            description=form.description.data,
            rating=form.rating.data,
            ranking=form.ranking.data,
            review=form.review.data,
            img_url=form.img_url.data
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
