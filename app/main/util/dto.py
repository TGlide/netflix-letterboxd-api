from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier', read_only=True)
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class MovieDto:
    api = Namespace('movie', description='movie related operations')
    movie = api.model('movie', {
        'id': fields.String(readonly=True, description='Movie id'),
        'title': fields.String(required=True, description='Movie title'),
        'countries': fields.String(required=False, description='Movie Countries'),
    })
