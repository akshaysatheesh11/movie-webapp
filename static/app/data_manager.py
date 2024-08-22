import sqlite3

from data_manager import DataManager

class DataManager:
    def __init__(self, db_name='moviweb.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            director TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL
        )''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_movies (
            user_id INTEGER,
            movie_id INTEGER,
            PRIMARY KEY (user_id, movie_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )''')

        self.conn.commit()

    def add_user(self, name):
        self.cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
        self.conn.commit()

    def add_movie(self, name, director, year, rating):
        self.cursor.execute('INSERT INTO movies (name, director, year, rating) VALUES (?, ?, ?, ?)',
                            (name, director, year, rating))
        self.conn.commit()

    def add_favorite(self, user_id, movie_id):
        self.cursor.execute('INSERT INTO user_movies (user_id, movie_id) VALUES (?, ?)', (user_id, movie_id))
        self.conn.commit()

    def remove_user(self, user_id):
        self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()

    def remove_movie(self, movie_id):
        self.cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
        self.conn.commit()

    def get_user_movies(self, user_id):
        self.cursor.execute('''
        SELECT movies.name, movies.director, movies.year, movies.rating
        FROM movies
        JOIN user_movies ON movies.id = user_movies.movie_id
        WHERE user_movies.user_id = ?''', (user_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
