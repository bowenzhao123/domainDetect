
from flask import Flask
from config import Config

def create_app(conf):
    app = Flask(__name__)
    app.config.from_object(conf)
    return app

conf = Config()
app = create_app(conf)


@app.route('/')
def home():
    return {'message':"ok"}, 200

from ftdview import *


if __name__ == '__main__':
    app.run(port=8802, debug=True)