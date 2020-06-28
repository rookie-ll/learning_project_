from APP.models.gift import Gift
from APP.webapp import web
from flask import render_template
from APP.ViewsModel.book import BookViewsModel
from flask_login import login_required


@web.route('/')
def index():
    recent_gift = Gift.recent()
    books = [BookViewsModel(book.book) for book in recent_gift]
    return render_template("index.html", recent=books)


@web.route('/personal')
def personal_center():
    return ""
