from flask import request, jsonify, current_app, render_template, flash, make_response

from APP.ViewsModel.trade import TradeInfo
from APP.models.gift import Gift
from APP.models.wish import Wish
from APP.webapp.libs import search_lib
from APP.webapp import web
from APP.webapp.libs.yushu_book import YuShuBook
from APP.froms.Search_from import SearchFrom
from APP.ViewsModel.book import BookCollection, BookViewsModel
import json


@web.route('/search/', methods=["GET"])
def search():
    form = SearchFrom(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data
        page = form.page.data
        is_isbn_or_key = search_lib.isbn_or_key(q)
        yushubook = YuShuBook()
        if is_isbn_or_key == "isbn":
            yushubook.search_by_isbn(q)
        else:
            yushubook.search_by_keyword(q, page)
        books.fill(yushubook, q)
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        # return jsonify(form.errors)
        flash("没有结果哦，亲爱的")
    return render_template("search_result.html", books=books, form=form)


@web.route('/book_detail/')
def book_detail():
    isbn = request.args.get("isbn")
    has_in_gift = False
    has_in_wish = False

    # 获取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewsModel(yushu_book.first)

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = TradeInfo(trade_gifts)
    trade_wishes = TradeInfo(trade_wishes)

    return render_template("book_detail.html", book=book, wishes=trade_wishes, gifts=trade_gifts,has_in_gift=has_in_gift,has_in_wish=has_in_wish)


@web.route("/set_cookie/")
def set_cookie():
    reponse = make_response("哈哈哈啊哈哈嗝")
    reponse.set_cookie("emmm", "asdf")
    return reponse
