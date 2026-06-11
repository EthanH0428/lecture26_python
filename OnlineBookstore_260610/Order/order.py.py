class Order:
    def __init__(self, order_id, member_id, items, total_price, address):
        self._order_id = order_id
        self._member_id = member_id
        self._items = items 
        self._total_price = total_price
        self._address = address

    def get_order_id(self): return self._order_id
    def get_member_id(self): return self._member_id

    def __str__(self):
        item_str = ", ".join([f"{title}({qty}개)" for _, title, qty in self._items])
        return f"주문번호: {self._order_id} | 주문내역: {item_str} | 총액: {self._total_price}원"