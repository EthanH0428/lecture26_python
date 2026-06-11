class Book:
    def __init__(self, book_id, title, author, price, stock):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._price = price
        self._stock = stock

    def get_book_id(self): return self._book_id
    def get_title(self): return self._title
    def get_author(self): return self._author
    def get_price(self): return self._price
    def get_stock(self): return self._stock
    def set_stock(self, stock): self._stock = stock

    def get_list_info(self):
        return f"[{self._book_id}] {self._title} - {self._author} | 가격: {self._price}원 | 재고: {self._stock}권"

    def __str__(self):
        return f"도서번호: {self._book_id}\n제목: {self._title}\n저자: {self._author}\n가격: {self._price}원\n재고: {self._stock}권"