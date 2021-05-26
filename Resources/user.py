from flask_restful import Resource
from flask import request
from flask_restful import reqparse
from flask_jwt_extended import create_access_token

from Model.user import UserModel


class User(Resource):

    def get(self):
        if request.args.get('id') is None and request.args.get('username') is None:
            return {'message': 'missing parameters'}, 400
        user = UserModel.find_user_by_id(request.args.get('id')) if UserModel.find_user_by_id(
            request.args.get('id')) else UserModel.find_by_username(request.args.get('username'))
        if user is None:
            return {'message': 'user not found'}, 404
        return user.json()


class UserRegister(Resource):
    # post with user as body - register
    def post(self):
        # search if the user exist, if it not we need to add
        new_user_data = request.get_json()
        name = new_user_data['username']
        if UserModel.find_by_username(username=name):
            return {'message': 'user with the username: {} already exist'.format(name)}, 400
        new_user = UserModel(username=new_user_data['username'], password=new_user_data['password'])
        try:
            new_user.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500
        return {'message': 'user added!', 'user': new_user.json()}


class Users(Resource):
    def get(self):
        db_users = UserModel.get_all_users()
        if db_users:
            users = {'users': list(map((lambda user: user.json()), db_users))}
            return users
        else:
            return {'message': 'Users list is empty'}, 400


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            return {'access_token': access_token}, 200
        return {"message": "Invalid Credentials!"}, 401
