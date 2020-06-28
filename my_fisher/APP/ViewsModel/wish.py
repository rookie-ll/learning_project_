from collections import namedtuple
from APP.ViewsModel.book import BookViewsModel

#MyGift = namedtuple("MyGift", ["id", "book", "wishes_count"])


class MyWishes:
    def __init__(self, gift_of_main, wish_count_list):
        self.gifts = []

        self.__gift_of_main = gift_of_main
        self.__wish_count_list = wish_count_list
        self.gifts = self._parse()

    def _parse(self):
        temp_list = []
        for gift in self.__gift_of_main:
            my_gift = self._matching(gift)
            temp_list.append(my_gift)
        return temp_list

    def _matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count.get("isbn"):
                count = wish_count.get("count")
        # my_gift = [MyGift(gift.id, BookViewsModel(gift.book), count)]
        r = {
            "id": gift.id,
            "book": BookViewsModel(gift.book),
            "wishes_count": count
        }
        return r
