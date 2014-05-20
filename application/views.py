import traceback

from flask import request
from flask.ext.restful import Resource

from application.models import FBUser
from application import fb


ERROR_CODES = {
    100: 'You must pass facebookId of person to add',
    101: 'Could not get user from Graph API',
    102: 'That user is already saved on db',
    200: 'You must pass the limit param',
    300: 'You must pass facebookId of person to remove',
    301: 'User does not exists',
    500: 'Unknown exception raised'
}


class Person(Resource):

    def post(self):
        facebook_id = request.form.get('facebookId')
        if not facebook_id:
            print 'Invalid facebook id passed in form'
            return {'error': ERROR_CODES[100], 'code': 100}, 400

        if FBUser.query.filter_by(facebook_id=facebook_id).first():
            print 'Facebook id {} already in db'.format(facebook_id)
            return {'error': ERROR_CODES[102], 'code': 102}, 403

        try:
            graph_user = fb.get_user(facebook_id)
        except ValueError:
            print 'Could not fetch user from graph api'
            print traceback.print_exc()
            return {'error': ERROR_CODES[101], 'code': 101}, 500
        except fb.FBError:
            print 'Could not fetch user from graph api'
            print traceback.print_exc()
            return {'error': ERROR_CODES[500], 'code': 500}, 500

        fb_user = FBUser(
            facebook_id=facebook_id,
            name=graph_user.get('name'),
            username=graph_user.get('username'),
            gender=graph_user.get('gender')
        )
        try:
            fb_user.add_and_commit()
        except Exception as err:
            error = ERROR_CODES[500]
            print 'Could not add user'
            print traceback.print_exc()
            return {'error': '{}: {}'.format(error, str(err)), 'code': 500}, 500

        print 'Added user {} successfully'.format(facebook_id)
        return {'result': fb_user.to_dict()}, 201

    def get(self):
        limit = request.args.get('limit')
        if not limit:
            return {'error': ERROR_CODES[200], 'code': 200}, 400

        users = [user.to_dict() for user in FBUser.query.limit(limit).all()]

        return {'result': users}, 200


class PersonDelete(Resource):

    def delete(self, facebook_id):
        if not facebook_id:
            print 'Invalid facebook id passed in form'
            return {'error': ERROR_CODES[300], 'code': 300}, 400

        fb_user = FBUser.query.filter_by(facebook_id=facebook_id).first()
        if not fb_user:
            print 'Cant delete facebook_id {} that is not on db.'.format(
                facebook_id
            )
            return {'error': ERROR_CODES[301], 'code': 301}, 404

        fb_user.remove_and_commit()

        print 'Deleted successfully facebook_id {}'.format(facebook_id)
        return {'result': 'OK'}, 204
