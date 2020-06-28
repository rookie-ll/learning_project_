class BookViewsModel(object):
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages']
        self.author = '、'.join(book['author'])
        self.price = book['price']
        self.isbn = book['isbn']
        self.summary = book['summary']
        self.image = book['image']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return ' / '.join(intros)


class BookCollection(object):
    def __init__(self):
        self.total = 0
        self.keyword = ""
        self.books = []

    def fill(self, yushubook, key):
        self.total = yushubook.total
        self.keyword = key
        self.books = [BookViewsModel(book) for book in yushubook.books]


class _BookViewsModel(object):
    @classmethod
    def isbn_filter(cls, data, keyword):
        returned = {
            "books": [],
            "search_key": keyword,
            "total": 0
        }
        if data:
            returned["total"] = 1
            returned["books"].append(cls._cat_keyword(data))
            # returned["books"]=[cls._cat_keyword(data)]
        return returned

    @classmethod
    def keyword_filter(cls, data, keyword):
        returned = {
            "books": [],
            "search_key": keyword,
            "total": 0
        }
        if data:
            returned["total"] = data.get("total")
            returned["books"] = [cls._cat_keyword(book) for book in data["books"]]
        return returned

    @classmethod
    def _cat_keyword(cls, data):
        book = {
            "title": data["title"],
            "publisher": data["publisher"],
            "pages": data["pages"],
            "author": "".join(data["author"]),
            "price": data["price"],
            "summary": data["summary"],
            "image": data["image"],
        }
        return book
