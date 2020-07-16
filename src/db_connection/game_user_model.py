# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from manage import app, db
from flask import Blueprint, request, jsonify

game_user = Blueprint(__name__)

class Game_User_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, unique=True, nullable=False)
    last_name = db.Column(db.String, unique=True, nullable=False)
    profile_pic = db.Column(db.String, unique=True, nullable=False)
    locale = db.Column(db.String, unique=True, nullable=False)
    timezone = db.Column(db.String, unique=True, nullable=False)
    gender = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return "<Game User: {}>".format(self.name)


    def get_all(self) ->dict:
        '''
        get all messages
        '''
        return Game_User_Model.query.all()

    def get_index(self, index: int) ->dict:
        '''
        retrieve message by index
        '''
        return Game_User_Model.query.get(index)

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

GUM = Game_User_Model()

@game_user.route('/add_user', methods=['POST'])
def create_new_game_user():
    try:
        req = request.get_json()
        user = Game_User_Model(first_name = req['first_name'], last_name = req['last_name'], profile_pic = req['profile_pic'] \n
        locale = req['locale'] timezone = req['timezone'] gender = req['gender'] )
        GUM.save(user)
        return jsonify(message='user added succesfully')

    except Exception as e:
	    return(str(e))



