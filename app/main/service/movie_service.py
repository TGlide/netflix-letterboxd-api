import uuid
import datetime

from app.main import db
from app.main.model.movie import Movie

from sqlalchemy import func, or_,  nullslast, desc, asc


def save_new_movie(data):
    movie = Movie.query.filter_by(
        title=data['title'].lower()).first()
    if not movie:
        try:
            new_movie = Movie(
                registered_on=datetime.datetime.utcnow(),
                title=data['title'].lower(),
                countries=data.get('countries', None)
            )
            save_changes(new_movie)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        except:
            response_object = {
                'status': 'fail',
                'message': 'API error fuck :(',
            }
            return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'Movie already exists.',
        }
        return response_object, 409


def delete_a_movie(movie):
    try:
        db.session.delete(movie)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.'
        }
        return response_object, 200
    except:
        response_object = {
            'status': 'fail',
            'message': f'Failed to delete movie.'
        }
        return response_object, 404


def get_all_movies(args):
    movies = Movie.query

    title = args.get('title', None)

    if title:
        movies = movies.filter(func.lower(Movie.title).contains(func.lower(
            title)))

    return movies.all()


def get_a_movie(id):
    return Movie.query.filter_by(id=id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
