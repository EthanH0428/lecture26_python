class BookService:
    def __init__(self, book_dao):
        self.book_dao = book_dao

    def add_book(self, title, author, price, stock):
        return self.book_dao.insert(title, author, price, stock)

    def get_all_books(self):
        return self.book_dao.select_all()

    def get_book_detail(self, book_id):
        return self.book_dao.select_by_id(book_id)

    def edit_book(self, book_id, book):
        return self.book_dao.update(book_id, book)

    def remove_book(self, book_id):
        return self.book_dao.delete(book_id)