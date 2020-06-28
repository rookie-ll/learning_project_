from APP.webapp.extends import db
from .http import Http
from flask import current_app
from APP.models.book import Book


class YuShuBook(object):
    isbn = "http://t.yushu.im/v2/book/isbn/{}"
    keyword = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    def __init__(self):
        self.books = []
        self.total = 0

    def search_by_isbn(self, isbn):
        url = self.isbn.format(isbn)
        # book = Book.query.filter(Book.isbn == isbn).paginate(page=1, per_page=15)
        # if book:
        #     return book
        # else:
        r = Http.get(url)
        self.modes(r)
        self._isbn_data(r)

    def _isbn_data(self, data):
        if data:
            self.books.append(data)
            self.total = 1

    def search_by_keyword(self, q, page=1):
        url = self.keyword.format(q, current_app.config.get("PER_PAGE"), self.start(page))
        # book = Book.query.filter(Book.title.ilike("%" + q + "%")).paginate(page=1, per_page=15)
        # if book:
        #     return book
        # else:
        r = Http.get(url)
        self.modes(r)
        self._keyword_data(r)

    def _keyword_data(self, data):
        if data:
            self.books = data["books"]
            self.total = data["total"]

    def start(self, page):
        return (page - 1) * current_app.config.get("PER_PAGE")

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else {}

    def modes(self, r):
        if r.get("books"):
            for data in r.get("books"):
                isbn = data.get("isbn")
                is_isbn = Book.query.filter(Book.isbn == isbn).first()
                if not is_isbn:
                    try:
                        book = Book(
                            title=data.get("title"),
                            author="".join(data.get("author")),
                            binding=data.get("binding"),
                            publisher=data.get("publisher"),
                            price=data.get("price"),
                            pages=data.get("pages"),
                            pubdate=data.get("pubdate"),
                            isbn=data.get("isbn"),
                            summary=data.get("summary"),
                            images=data.get("image")
                        )
                        db.session.add(book)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        raise e
