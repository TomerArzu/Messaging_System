
from base import BaseModel, db

class MessageModel(db.Model, BaseModel):
    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    subject = db.Column(db.String(10))
    content = db.Column(db.String(10))

    receiver_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    receiver = db.relationship('UserModel')
    sender = db.Column(db.Integer)

    def __init__(self, sender, receiver_id, creation_date, is_read, subject, content, _id=None):
        self.id = _id
        self.receiver_id = receiver_id
        self.sender = sender
        self.creation_date = creation_date
        self.is_read = is_read
        self.subject = subject
        self.content = content

    @classmethod
    def get_by_id(cls, msg_id):
        return cls.query.filter_by(id=msg_id).first()

    @classmethod
    def mark_as_read(cls):
        if not cls.is_read:
            cls.is_read = True
            read_msg = MessageModel(cls.receiver_id, cls.sender, cls.creation_date, cls.is_read, cls.subject,
                                    cls.content,
                                    cls.id)
            read_msg.save_to_db()

    @classmethod
    def unread_messages(cls, sender):
        return cls.query.filter_by(sender=sender).filter_by(is_read=False).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id': self.id,
                'sender': self.sender,
                'receiver': self.receiver_id,
                'creation_date': self.creation_date.strftime("%m/%d/%Y, %H:%M:%S"),
                'is_read': self.is_read,
                'subject': self.subject,
                'content': self.content}
