from flask import Blueprint, jsonify
from first.utils import *

first_blueprint = Blueprint('first_blueprint', __name__)
data = SearchDAO('netflix.db')

@first_blueprint.route('/movie/<title>')
def title_movie(title):
    search = data.search_by_title(title)
    return jsonify(search)


@first_blueprint.route('/movie/<int:year_1>/to/<int:year_2>')
def search_movie(year_1, year_2):
    search = data.search_by_year(year_1, year_2)
    return jsonify(search)


@first_blueprint.route('/rating/<str>')
def search_rating(str):
    search = data.search_by_rating(str)
    return jsonify(search)

@first_blueprint.route('/genre/<genre>')
def search_genre(genre):
    search = data.search_by_genre(genre)
    return jsonify(search)

