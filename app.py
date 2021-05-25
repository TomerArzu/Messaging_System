# flask imports
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_jwt_extended import JWTManager
# for jwt
from Resources.user import User, UserRegister, Users, UserLogin
from Resources.message import Message, Messages

app = Flask(__name__)
api = Api(app)
# todo: put in os env variables on heruko
app.secret_key = 'tomer_arzuan'
# configs for application
# track of modification that we do in db session but we already have a modification tracker in flask_sqlAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messaging_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


jwt = JWTManager(app)



api.add_resource(UserRegister, '/signup')
api.add_resource(UserLogin, '/login')
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/user')
api.add_resource(Message, '/api/user/message')
api.add_resource(Messages, '/api/user/messages')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
