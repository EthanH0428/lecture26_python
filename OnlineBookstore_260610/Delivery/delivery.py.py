class Delivery:
    def __init__(self, delivery_id, order_id, member_id, address, status="배송준비중"):
        self._delivery_id = delivery_id
        self._order_id = order_id
        self._member_id = member_id
        self._address = address
        self._status = status

    def get_delivery_id(self): return self._delivery_id
    def get_order_id(self): return self._order_id
    def get_member_id(self): return self._member_id
    def get_status(self): return self._status
    def set_status(self, status): self._status = status

    def __str__(self):
        return f"배송번호: {self._delivery_id} | 주문번호: {self._order_id} | 배송지: {self._address} | 상태: {self._status}"