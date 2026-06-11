class CartService:
    def __init__(self, cart_dao, cart_item_dao, book_service):
        self.cart_dao = cart_dao
        self.cart_item_dao = cart_item_dao
        self.book_service = book_service

    def add_item(self, member_id, book_id, quantity):
        if quantity <= 0:
            return 'QUANTITY_ERROR'
        book = self.book_service.get_book_detail(book_id)
        if not book:
            return 'NOT_FOUND'
        if book.get_stock() < quantity:
            return 'STOCK_ERROR'
        
        return self.cart_item_dao.save_item(member_id, book_id, quantity)

    def remove_item(self, member_id, book_id, quantity):
        return self.cart_item_dao.remove_item(member_id, book_id, quantity)

    def view_cart(self, member_id):
        cart_data = self.cart_dao.get_cart(member_id)
        if not cart_data:
            return None
        
        result = "============ 장바구니 품목 ============\n"
        total_price = 0
        for book_id, qty in cart_data.items():
            book = self.book_service.get_book_detail(book_id)
            if book:
                item_price = book.get_price() * qty
                total_price += item_price
                result += f"[{book.get_book_id()}] {book.get_title()} | 수량: {qty}개 | 금액: {item_price}원\n"
        result += f"=======================================\n총 주문 금액: {total_price}원"
        return result