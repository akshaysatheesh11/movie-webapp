from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movieweb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    reviews = db.relationship('Review', backref='user', lazy=True)

class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    director_id = db.Column(db.Integer, db.ForeignKey('directors.director_id'))
    rating = db.Column(db.Float)
    reviews = db.relationship('Review', backref='movie', lazy=True)

class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    movies = db.relationship('Movie', backref='genre', lazy=True)

class Director(db.Model):
    __tablename__ = 'directors'
    director_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    movies = db.relationship('Movie', backref='director', lazy=True)

class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/movies/<int:movie_id>')
def view_movie(movie_id):
    movie = Movie.query.get(movie_id)
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return render_template('view_movie.html', movie=movie, reviews=reviews)

@app.route('/movies/<int:movie_id>/add_review', methods=['GET', 'POST'])
def add_review(movie_id):
    if request.method == 'POST':
        user_id = request.form['user_id']
        review_text = request.form['review_text']
        rating = request.form['rating']
        new_review = Review(user_id=user_id, movie_id=movie_id, review_text=review_text, rating=rating)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('view_movie', movie_id=movie_id))
    return render_template('add_review.html', movie_id=movie_id)

@app.route('/add_director', methods=['GET', 'POST'])
def add_director():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        new_director = Director(name=name, birth_date=birth_date)
        db.session.add(new_director)
        db.session.commit()
        return redirect(url_for('list_directors'))
    return render_template('add_director.html')

@app.route('/directors')
def list_directors():
    directors = Director.query.all()
    return render_template('list_directors.html', directors=directors)

@app.route('/add_genre', methods=['GET', 'POST'])
def add_genre():
    if request.method == 'POST':
        name = request.form['name']
        new_genre = Genre(name=name)
        db.session.add(new_genre)
        db.session.commit()
        return redirect(url_for('list_genres'))
    return render_template('add_genre.html')

@app.route('/genres')
def list_genres():
    genres = Genre.query.all()
    return render_template('list_genres.html', genres=genres)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
