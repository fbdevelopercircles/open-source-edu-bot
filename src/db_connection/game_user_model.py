# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from manage import app, db

class Game_User_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String, unique=True, nullable=False)
    profile_pic = db.Column(db.String, unique=True, nullable=False)
    locale = db.Column(db.String, unique=True, nullable=False)
    timezone = db.Column(db.String, unique=True, nullable=False)
    gender = db.Column(db.String, unique=True, nullable=False)


