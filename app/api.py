import flask
import json
from flask import request, jsonify
import movie_suggestion as movie


app = flask.Flask(__name__)
app.config["DEBUG"] = True
movie_df = movie.moviesuggestion()
# Create some test data for our catalog in the form of a list of dictionaries.



@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/movie_suggestion/similiar_names/<movie>', methods=['GET'])
def api_similar_name(movie):
    df = movie_df.get_similiar_named_movies(movie)
    print(df.columns)
    return jsonify(json.loads(df.to_json(orient='records')))

@app.route('/api/movie_suggestion/keywords/<movie>',methods=['GET'])
def api_similar_keywords(movie):
    name = movie_df.get_similiar_named_movies(movie)['title'].values[0].lower()
    df = movie_df.get_movies_by_keywords(name)
    return jsonify(json.loads(df.to_json(orient='records')))

@app.route('/api/movie_suggestion/content/<movie>',methods=['GET'])
def api_similar_content(movie):
    name = movie_df.get_similiar_named_movies(movie)['title'].values[0].lower()
    df = movie_df.get_movies_by_content(name)
    return jsonify(json.loads(df.to_json(orient='records')))



