from dao import MemberDAO, ProductDAO
from model import Cart, Order, OrderItem

class ShopService:
    def __init__(self):
        self.member_dao = MemberDAO()
        self.product_dao = ProductDAO()
        self.cart = Cart()
        self.orders = []
        self.logined_member = None
        self.order_sequence = 20260001  

    def login(self, login_id: str, password: str) -> bool:
        member = self.member_dao.find_by_login_id(login_id)
        if member and member.password == password:
            self.logined_member = member
            return True
        return False

    def get_product_list(self) -> list:
        return self.product_dao.find_all()

    def add_to_cart(self, product_id: int, qty: int):
        product = self.product_dao.find_by_id(product_id)
        if not product:
            raise ValueError("존재하지 않는 상품입니다.")
        self.cart.add_item(product, qty)

    def create_order(self) -> Order:
        if not self.cart.items:
            raise ValueError("장바구니가 비어있습니다.")
        
        order_items = []
        for cart_item in self.cart.items:
            product = cart_item.product
     
            product.decrease_stock(cart_item.get_quantity) if hasattr(cart_item, 'get_quantity') else product.decrease_stock(cart_item.quantity)
            order_items.append(OrderItem(product, cart_item.quantity))

        order_no = str(self.order_sequence)
        self.order_sequence += 1
        tracking_no = f"TRK-{order_no}"
        
        order = Order(order_no, self.logined_member, order_items, tracking_no)
        self.orders.append(order)
        self.cart.clear()  # 주문 성공 후 장바구니 초기화
        return order

class AdminService:
    def __init__(self, shop_service: ShopService):
        self.shop_service = shop_service

    def get_total_sales(self) -> int:
        return sum(order.total_amount for order in self.shop_service.orders)

    def get_total_order_count(self) -> int:
        return len(self.shop_service.orders)