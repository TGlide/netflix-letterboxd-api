from ..service.movie_service import save_new_movie, get_all_movies, get_a_movie, delete_a_movie, get_movies_from_letterboxd, get_movies_from_letterboxd_list
from ..util.dto import MovieDto
from ..util.decorator import token_required, admin_token_required

from flask_restplus import Resource
from flask import request


api = MovieDto.api
_movie = MovieDto.movie


@api.route('/')
@api.param('title', 'Search by title')
class MovieList(Resource):
    @api.doc('list_of_registered_movies')
    @api.marshal_list_with(_movie, envelope='data')
    def get(self):
        """List all registered movies"""
        return get_all_movies(request.args)

    @api.response(201, 'Movie successfully created.')
    @api.doc('create a new movie')
    @api.expect(_movie, validate=False)
    @admin_token_required
    def post(self):
        """Creates a new Movie """
        data = request.json
        return save_new_movie(data=data)


@api.route('/<id>')
@api.param('id', 'The Movie identifier')
@api.response(404, 'Movie not found.')
class Movie(Resource):
    @api.doc('get a movie')
    @api.marshal_with(_movie)
    def get(self, id):
        """get a movie given its identifier"""
        movie = get_a_movie(id)
        if not movie:
            api.abort(404)
        else:
            return movie

    @api.doc('delete a movie')
    @admin_token_required
    def delete(self, id):
        """delete a movie given its identifier"""
        movie = get_a_movie(id)
        if not movie:
            api.abort(404)
        else:
            return delete_a_movie(movie)


@api.route('/watchlist/<owner>')
@api.param('owner', 'The watchlist owner username')
class Letterboxd(Resource):
    @api.doc('get movies from a letterboxd list')
    def get(self, owner):
        """get movies from a list given the list owner"""
        movies = get_movies_from_letterboxd(owner)
        if not movies:
            api.abort(404)
        else:
            return movies


@api.route('/list/<owner>/<list_name>')
@api.param('owner', 'The letterboxd list owner')
@api.param('list_name', 'The letterboxd list name')
class Letterboxd(Resource):
    @api.doc('get movies from a letterboxd list')
    def get(self, owner, list_name):
        """get movies from a list given the owner and the list name"""
        movies = get_movies_from_letterboxd_list(owner, list_name)
        if not movies:
            api.abort(404)
        else:
            return movies
