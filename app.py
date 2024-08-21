from flask import Flask, request, jsonify
from data_manager import DataManager

app = Flask(__name__)
dm = DataManager()

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.json.get('name')
    dm.add_user(name)
    return jsonify({"status": "User added"}), 201

@app.route('/add_movie', methods=['POST'])
def add_movie():
    data = request.json
    dm.add_movie(data['name'], data['director'], data['year'], data['rating'])
    return jsonify({"status": "Movie added"}), 201

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    data = request.json
    dm.add_favorite(data['user_id'], data['movie_id'])
    return jsonify({"status": "Favorite added"}), 201

@app.route('/get_user_movies/<int:user_id>', methods=['GET'])
def get_user_movies(user_id):
    movies = dm.get_user_movies(user_id)
    return jsonify(movies)

if __name__ == '__main__':
    app.run(debug=True)
