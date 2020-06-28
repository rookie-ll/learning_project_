from flask import Flask
from APP.webapp import web
from APP.secure import Secures
from APP.settings import Setings
from APP.webapp.extends import ext_app
from APP import models


def create_app():
    app = Flask(__name__)

    app.config.from_object(Secures)
    app.config.from_object(Setings)

    app.register_blueprint(web, url_perfix="/book")

    ext_app(app)

    return app
