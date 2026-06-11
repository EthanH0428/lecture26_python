class OrderService:
    def __init__(self, order_dao, order_item_dao, cart_service, delivery_service):
        self.order_dao = order_dao
        self.order_item_dao = order_item_dao
        self.cart_service = cart_service
        self.delivery_service = delivery_service

    def get_member_address(self, member_id):
        # 기존 배송 이력이 있다면 마지막 배송지 반환
        deliveries = self.delivery_service.view_member_deliveries(member_id)
        if deliveries:
            return deliveries[-1]._address
        return None

    def order_cart(self, member_id, address):
        cart_data = self.cart_service.cart_dao.get_cart(member_id)
        if not cart_data:
            return 'EMPTY_CART'
        
        # 재고 검증 및 주문 상품 리스트업
        order_items = []
        total_price = 0
        
        for book_id, qty in cart_data.items():
            book = self.cart_service.book_service.get_book_detail(book_id)
            if not book or book.get_stock() < qty:
                return 'STOCK_ERROR'
            order_items.append((book_id, book.get_title(), qty))
            total_price += book.get_price() * qty

        # 재고 차감 및 주문 확정
        for book_id, _, qty in order_items:
            book = self.cart_service.book_service.get_book_detail(book_id)
            book.set_stock(book.get_stock() - qty)

        # 주문 및 배송 엔티티 생성
        order = self.order_dao.insert(member_id, order_items, total_price, address)
        self.delivery_service.create_delivery(order.get_order_id(), member_id, address)
        
        # 장바구니 비우기
        self.cart_service.cart_dao.clear_cart(member_id)
        return True

    def get_member_orders(self, member_id):
        return self.order_dao.select_by_member(member_id)

    def get_order_detail(self, order_id):
        return self.order_dao.select_by_id(order_id)

    def get_all_orders(self):
        return self.order_dao.select_all()

    def cancel_order(self, order_id):
        order = self.order_dao.select_by_id(order_id)
        if not order:
            return False
        
        # 배송상태 확인 (배송 시작 이후엔 취소 불가 유효성 검증)
        delivery = self.delivery_service.view_delivery_by_order(order_id)
        if delivery and delivery.get_status() != "배송준비중":
            return False

        # 책 재고 원복 복구
        for book_id, _, qty in order._items:
            book = self.cart_service.book_service.get_book_detail(book_id)
            if book:
                book.set_stock(book.get_stock() + qty)
                
        return self.order_dao.delete(order_id)