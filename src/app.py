from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    from os import environ
    app.run(debug=False, port=environ.get("PORT", 5000))
