# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from manage import app, db

class Messages_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, unique=True, nullable=False)
    message_triggers = db.Column(db.String, unique=True, nullable=False)
    message_payload = db.Column(db.String, unique=True, nullable=False)
