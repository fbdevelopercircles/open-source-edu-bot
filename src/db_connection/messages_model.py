# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from manage import app, db
from flask import Blueprint, request, jsonify

messages = Blueprint(__name__)

class Messages_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, unique=True, nullable=False)
    message_triggers = db.Column(db.String, unique=True, nullable=False)
    message_payload = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return "<Messages: {}>".format(self.message)


    def get_all(self) ->dict:
        '''
        get all messages
        '''
        return Messages_Model.query.all()

    def get_index(self, index: int) ->dict:
        '''
        retrieve message by index
        '''
        return Messages_Model.query.get(index)

    def get_payload(self, payload: str) ->dict:
        '''
        retrieve message by payload
        '''
        return Messages_Model.query.filter_by(message_payload=payload).first()


    def save(self, entity):
        '''
        save data to db
        '''
        db.session.add(entity)
        db.session.commit()


    def delete(self, id: int):
        '''
        delete data from db
        '''
        db.session.delete(id)
        db.session.commit()

#-------------------------------------------------------------------------------------------------------

MM = Messages_Model()

@messages.route('/add_messages', methods=['POST'])
def create_new_message():
    try:
        req = request.get_json()
        message = Messages_Model(message = req['message'], message_payload = req['message_payload'], message_trigger = req['message_trigger'])
        MM.save(message)
        return jsonify(message='Message added succesfully')

    except Exception as e:
	    return(str(e))
