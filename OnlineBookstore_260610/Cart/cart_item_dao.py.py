class CartItemDAO:
    def __init__(self, cart_dao):
        self.cart_dao = cart_dao

    def save_item(self, member_id, book_id, quantity):
        cart = self.cart_dao.get_cart(member_id)
        if book_id in cart:
            cart[book_id] += quantity
        else:
            cart[book_id] = quantity
        return True

    def remove_item(self, member_id, book_id, quantity):
        cart = self.cart_dao.get_cart(member_id)
        if book_id not in cart:
            return 'NOT_FOUND'
        if cart[book_id] < quantity:
            return 'QUANTITY_ERROR'
        
        cart[book_id] -= quantity
        if cart[book_id] <= 0:
            del cart[book_id]
        return True