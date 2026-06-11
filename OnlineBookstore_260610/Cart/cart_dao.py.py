class CartDAO:
    def __init__(self):
        # 구조: { member_id: { book_id: quantity } }
        self._carts = {}

    def get_cart(self, member_id):
        if member_id not in self._carts:
            self._carts[member_id] = {}
        return self._carts[member_id]

    def clear_cart(self, member_id):
        if member_id in self._carts:
            self._carts[member_id] = {}