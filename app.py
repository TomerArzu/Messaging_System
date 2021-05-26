from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from Resources.user import User, UserRegister, Users, UserLogin
from Resources.message import Message, Messages

app = Flask(__name__)
api = Api(app)
app.secret_key = 'tomer_arzuan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messaging_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)

api.add_resource(UserRegister, '/signup')
api.add_resource(UserLogin, '/login')
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/user')
api.add_resource(Message, '/api/user/message')
api.add_resource(Messages, '/api/user/messages')


@jwt.expired_token_loader
def handle_auth_error_callback():
    return jsonify({'message': 'token expired !'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': 'signature verification failed'}), 401


@jwt.unauthorized_loader
def unauthorized_callback():
    return jsonify({'message': 'not authorized'}), 401


if __name__ == "__main__":
    app.run(port=5002, debug=True)
