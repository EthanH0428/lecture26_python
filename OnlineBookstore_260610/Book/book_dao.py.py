class BookDAO:
    def __init__(self):
        self._books = {}
        self._counter = 1

    def insert(self, title, author, price, stock):
        book_id = str(self._counter)
        from Book.book import Book
        self._books[book_id] = Book(book_id, title, author, price, stock)
        self._counter += 1
        return True

    def select_by_id(self, book_id):
        return self._books.get(book_id)

    def select_all(self):
        return list(self._books.values())

    def update(self, book_id, updated_book):
        if book_id in self._books:
            self._books[book_id] = updated_book
            return True
        return False

    def delete(self, book_id):
        if book_id in self._books:
            del self._books[book_id]
            return True
        return False