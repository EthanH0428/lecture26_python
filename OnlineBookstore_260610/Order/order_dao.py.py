class OrderDAO:
    def __init__(self):
        self._orders = {}
        self._counter = 5001

    def insert(self, member_id, items, total_price, address):
        from Order.order import Order
        o_id = str(self._counter)
        order = Order(o_id, member_id, items, total_price, address)
        self._orders[o_id] = order
        self._counter += 1
        return order

    def select_by_id(self, order_id):
        return self._orders.get(order_id)

    def select_by_member(self, member_id):
        return [o for o in self._orders.values() if o.get_member_id() == member_id]

    def select_all(self):
        return list(self._orders.values())

    def delete(self, order_id):
        if order_id in self._orders:
            del self._orders[order_id]
            return True
        return False