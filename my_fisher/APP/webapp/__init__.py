from flask import Blueprint

web = Blueprint("web", __name__, template_folder="templates")

from .views import auth, book, drift, gift, main, wish
