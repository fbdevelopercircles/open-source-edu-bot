# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os


from flask import Flask, request, Response, g
from flask_babel import Babel

babel = Babel()


def create_app(test_config=None):
    # The app factory function

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'fbosbot.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    babel.init_app(app)
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'

    # path = os.getcwd()
    # locales_path = os.path.abspath(os.path.join(path, os.pardir, 'locales'))
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = "../locales"

    from services import messenger
    app.register_blueprint(messenger.bp)
    app.add_url_rule('/webhook', endpoint='webhook')

    return app
