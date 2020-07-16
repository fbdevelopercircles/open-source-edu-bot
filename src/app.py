# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
from manage import app, db
from services.messenger import bp

app.register_blueprint(bp)
app.add_url_rule('/webhook', endpoint='webhook')

with app.app_context():
    from db_connection.game_user_model import Game_User_Model
    from db_connection.messages_model import Messages_Model
    db.init_app(app)
    db.create_all()


@app.route('/')
def hello():
    return 'Health Check'

if __name__ == '__main__':
    app.run(debug=False, port=os.environ.get("PORT", 5000))