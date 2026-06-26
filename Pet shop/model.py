from datetime import datetime

class Member:
    def __init__(self, id: int, login_id: str, password: str, name: str, grade: str):
        self.id = id
        self.login_id = login_id
        self.password = password
        self.name = name
        self.grade = grade # 예: SILVER

class Product:
    def __init__(self, id: int, name: str, price: int, stock: int, description: str):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.description = description

    def decrease_stock(self, qty: int):
        if self.stock < qty:
            raise ValueError("재고가 부족합니다.")
        self.stock -= qty

class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def get_subtotal(self) -> int:
        return self.product.price * self.quantity

    def add_quantity(self, qty: int):
        self.quantity += qty

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product: Product, qty: int):
        for item in self.items:
            if item.product.id == product.id:
                item.add_quantity(qty)
                return
        self.items.append(CartItem(product, qty))

    def get_total_price(self) -> int:
        return sum(item.get_subtotal() for item in self.items)

    def clear(self):
        self.items.clear()

class OrderItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.order_price = product.price  # 주문 시점의 가격 보관
        self.quantity = quantity

    def get_subtotal(self) -> int:
        return self.order_price * self.quantity

class Order:
    def __init__(self, order_no: str, member: Member, order_items: list, tracking_no: str):
        self.order_no = order_no
        self.member = member
        self.order_items = order_items
        self.total_amount = sum(item.get_subtotal() for item in order_items)
        self.delivery_status = "PREPARING"
        self.tracking_no = tracking_no