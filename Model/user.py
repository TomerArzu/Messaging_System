from db import db


class UserModel(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(10))

    messages = db.relationship('MessageModel', lazy= 'dynamic')
    # receiver_message = db.relationship('MessageModel')
    # messages_senders = db.relationship('MessageModel', backref='sender', lazy=True)
    # messages_receivers = db.relationship('MessageModel', backref='receiver')

    def __init__(self, username, password, _id=None):
        self.id = _id
        self.username = username
        self.password = password if password else None

    # insert new user to db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    @classmethod
    def get_unread_msgs(cls):
        return cls.messages.filter_by(is_read=False).all()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    # return json representation of User
    def json(self):
        return {'id': self.id,
                'username': self.username}
