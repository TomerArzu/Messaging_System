from flask_restful import Resource
from flask import request
from flask_restful import reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from Model.message import MessageModel
from Model.user import UserModel
from datetime import datetime


class Message(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)
        if user:
            if request.args.get('id'):
                db_message = user.messages.filter_by(id=request.args.get('id')).first()
                if db_message:
                    response = db_message.json()
                    if not db_message.is_read:
                        db_message.is_read = True
                        db_message.save_to_db()
                    return response
            return {'message': 'Message did not found'}, 404
        return {'message': 'user did not found'}, 404

    # POST
    # write new message
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)
        if user:
            new_msg_data = request.get_json()
            if UserModel.find_user_by_id(new_msg_data['receiver']):
                new_msg = MessageModel(sender=user_id, receiver_id=new_msg_data['receiver'],
                                       creation_date=datetime.utcnow(), is_read=False, subject=new_msg_data['subject'],
                                       content=new_msg_data['content'])
                new_msg.save_to_db()
            else:
                return {'message': 'you try to send to un-exist user, try again'}, 400
            return {'message': "message sent!", "message_id": f"{new_msg.json()['id']}"}
        return {'message': 'user did not found'}, 404

    # DELETE
    @jwt_required()
    def delete(self):
        user_id= get_jwt_identity()
        # check if user connect
        # check if the message exist and belong to this user and delete
        user= UserModel.find_user_by_id(user_id)
        if user:
            if request.args.get('id'):
                db_message = user.messages.filter_by(id=request.args.get('id')).first()
                if db_message:
                    db_message.delete()
                else:
                    return {'message': 'Message did not found'},404
            else:
                return {'message': 'missing parameters'}, 400
        else:
            return {'message': 'user not found'}, 404
        return {'message': 'Message deleted !'}


class Messages(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)
        if user:
            unread = bool(request.args.get('unread')) if request.args.get('unread') else False
            if unread:
                return {'unread messages': {'Total': user.messages.filter_by(is_read=False).count(),
                                            'messages id': list(map((lambda message: {'id': message.json()['id'],
                                                                                      'sender': message.json()[
                                                                                          'sender'],
                                                                                      'sent date': message.json()[
                                                                                          'creation_date']}),
                                                                    user.messages.filter_by(is_read=False).all()))}}
            else:
                return {'all messages': {'Total': user.messages.count(),
                                         'messages': list(map((lambda message: {'id': message.json()['id'],
                                                                                'sender': message.json()['sender'],
                                                                                'sent date': message.json()[
                                                                                    'creation_date']}),
                                                              user.messages.all()))}}
