from datetime import datetime
from enum import Enum
from typing import List, Optional

# ==========================================
# 1. 도메인 모델 & 비즈니스 로직 (클래스 다이어그램 반영)
# ==========================================

class Grade(Enum):
    SILVER = "SILVER"
    GOLD = "GOLD"
    VIP = "VIP"

class OrderStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class DeliveryStatus(Enum):
    PREPARING = "PREPARING"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"


class Category:
    def __init__(self, cat_id: int, name: str):
        self.id = cat_id
        self.name = name


class Product:
    def __init__(self, prod_id: int, name: str, price: int, stock: int, description: str, category: Category):
        self.id = prod_id
        self.name = name
        self.price = price
        self.stock = stock
        self.description = description
        self.category = category

    def decreaseStock(self, qty: int) -> None:
        if self.stock < qty:
            raise ValueError(f"❌ [재고 부족] {self.name}의 재고가 부족합니다. (현재 재고: {self.stock}개)")
        self.stock -= qty

    def isAvailable(self) -> bool:
        return self.stock > 0


class Member:
    def __init__(self, member_id: int, login_id: str, password: str, name: str, address: str):
        self.id = member_id
        self.loginId = login_id
        self.password = password
        self.name = name
        self.address = address
        self.grade = Grade.SILVER
        self.cart: Optional['Cart'] = None

    def login(self, login_id: str, password: str) -> bool:
        return self.loginId == login_id and self.password == password


class CartItem:
    def __init__(self, item_id: int, product: Product, quantity: int):
        self.id = item_id
        self.product = product
        self.quantity = quantity

    def subtotal(self) -> int:
        return self.product.price * self.quantity


class Cart:
    def __init__(self, cart_id: int, member: Member):
        self.id = cart_id
        self.member = member
        self.items: List[CartItem] = []
        self.member.cart = self

    def addItem(self, product: Product, qty: int) -> None:
        if qty <= 0:
            print("❌ 수량은 1개 이상이어야 합니다.")
            return
        if product.stock < qty:
            print(f"❌ 재고가 부족합니다. (현재 재고: {product.stock}개)")
            return
            
        for item in self.items:
            if item.product.id == product.id:
                if product.stock < (item.quantity + qty):
                    print(f"❌ 장바구니에 담긴 수량({item.quantity}개) + 추가 수량({qty}개)이 현재 재고({product.stock}개)를 초과합니다.")
                    return
                item.quantity += qty
                print(f"🛒 {product.name}의 수량이 {item.quantity}개로 변경되었습니다.")
                return
                
        new_item = CartItem(item_id=len(self.items) + 1, product=product, quantity=qty)
        self.items.append(new_item)
        print(f"🛒 {product.name} {qty}개가 장바구니에 담겼습니다.")

    def clearCart(self) -> None:
        self.items = []

    def totalPrice(self) -> int:
        return sum(item.subtotal() for item in self.items)


class Delivery:
    def __init__(self, del_id: int, address: str):
        self.id = del_id
        self.address = address
        self.status = DeliveryStatus.PREPARING
        self.trackingNo = f"TRK-{del_id:04d}"


class OrderItem:
    def __init__(self, item_id: int, product: Product, order_price: int, quantity: int):
        self.id = item_id
        self.product = product
        self.orderPrice = order_price
        self.quantity = quantity

    def subtotal(self) -> int:
        return self.orderPrice * self.quantity


class Order:
    def __init__(self, order_id: int, member: Member, delivery_address: str, order_items: List[OrderItem]):
        self.id = order_id
        self.orderDate = datetime.now()
        self.status = OrderStatus.PENDING
        self.member = member
        self.orderItems = order_items
        
        # 주문 시점에 실제 재고 차감 (비즈니스 로직 연동)
        for item in self.orderItems:
            item.product.decreaseStock(item.quantity)
            
        self.totalAmount = self.calcTotal()
        self.delivery = Delivery(del_id=order_id, address=delivery_address)
        self.status = OrderStatus.PAID

    def calcTotal(self) -> int:
        return sum(item.subtotal() for item in self.orderItems)


class Review:
    def __init__(self, rev_id: int, rating: int, content: str, member: Member, product: Product):
        self.id = rev_id
        self.rating = rating
        self.content = content
        self.writtenAt = datetime.now()
        self.member = member
        self.product = product


# ==========================================
# 2. 인터랙티브 웹 쇼핑몰 UI 및 실행부
# ==========================================

def run_shop_simulation():
    # 마스터 데이터 세팅
    cat = Category(1, "반려동물 용품")
    products = [
        Product(1, "유기농 연어 사료 2kg", 35000, 10, "눈물 개선에 좋은 최고급 사료", cat),
        Product(2, "치석 제거 덴탈껌 30P", 12000, 20, "매일 즐겁게 하는 치아 관리", cat),
        Product(3, "고양이 캣닙 스크래쳐", 18000, 5, "스트레스 해소용 고밀도 스크래쳐", cat)
    ]
    
    # 가상 회원 정보 구축 (로그인용)
    current_user = Member(101, "test", "1234", "김싸피", "서울시 강남구 역삼동")
    cart = Cart(cart_id=501, member=current_user)
    
    orders: List[Order] = []
    reviews: List[Review] = []

    print("=" * 60)
    print("🐾 안녕하세요! 'Ethan의 반려용품 온라인 숍'에 오신 것을 환영합니다.")
    print("Welcome to Ethans Pet Shop!!")
    print("=" * 60)

    # 단순화를 위한 가상 로그인 프로세스
    while True:
        print("\n🔐 [로그인 화면]")
        input_id = input("- 아이디 입력: ").strip()
        input_pw = input("- 비밀번호 입력: ").strip()
        
        if current_user.login(input_id, input_pw):
            print(f"\n🎉 로그인 성공! {current_user.name} 님 반갑습니다. (등급: {current_user.grade.value})")
            break
        else:
            print("❌ 아이디 또는 비밀번호가 틀렸습니다. 다시 시도해 주세요.")


    while True:
        print("\n" + "=" * 25 + " [메인 메뉴] " + "=" * 25)
        print("1. 상품 목록 조회 및 담기 (상품 / 장바구니 메뉴)")
        print("2. 장바구니 확인 및 주문하기 (장바구니 / 주문 메뉴)")
        print("3. 주문 내역 및 배송 조회 (주문·배송 / 마이페이지 메뉴)")
        print("4. 구매 상품 리뷰 작성하기 (상품 / 마이페이지 메뉴)")
        print("5. [관리자 모드] 재고 및 매출 현황 확인")
        print("0. 쇼핑몰 종료")
        print("=" * 63)
        
        choice = input("👉 원하시는 메뉴 번호를 입력하세요: ").strip()

        # 1. 상품 조회 및 장바구니 담기
        if choice == "1":
            print("\n🛒 [상품 목록]")
            for p in products:
                status = f"{p.stock}개 남음" if p.isAvailable() else "🚨 품절"
                print(f" [{p.id}] {p.name} | 가격: {p.price}원 | 재고: {status}\n     설명: {p.description}")
            
            print("-" * 40)
            try:
                p_id = int(input("장바구니에 담을 상품의 번호를 입력하세요 (취소하려면 0): "))
                if p_id == 0: continue
                
                selected_prod = next((p for p in products if p.id == p_id), None)
                if not selected_prod:
                    print("❌ 존재하지 않는 상품 번호입니다.")
                    continue
                
                qty = int(input(f"'{selected_prod.name}'을 몇 개 담으시겠습니까?: "))
                cart.addItem(selected_prod, qty)
            except ValueError:
                print("❌ 올바른 숫자를 입력해 주세요.")

        # 2. 장바구니 확인 및 주문하기
        elif choice == "2":
            print("\n🧺 [나의 장바구니]")
            if not cart.items:
                print("장바구니가 비어 있습니다. 상품을 먼저 담아보세요!")
                continue
                
            for item in cart.items:
                print(f" - {item.product.name} : {item.quantity}개 = {item.subtotal()}원")
            print(f"💰 총 예상 결제 금액: {cart.totalPrice()}원")
            print("-" * 40)
            
            pay_choice = input("💳 현재 장바구니 상태로 주문을 진행하시겠습니까? (Y/N): ").strip().upper()
            if pay_choice == 'Y':
                try:
                    order_items = []
                    for idx, cart_item in enumerate(cart.items):
                        oi = OrderItem(
                            item_id=idx + 1, 
                            product=cart_item.product, 
                            order_price=cart_item.product.price, 
                            quantity=cart_item.quantity
                        )
                        order_items.append(oi)
                    

                    new_order = Order(
                        order_id=20260000 + len(orders) + 1, 
                        member=current_user, 
                        delivery_address=current_user.address, 
                        order_items=order_items
                    )
                    orders.append(new_order)
                    
                    print(f"\n✅ 주문 및 결제가 완료되었습니다!")
                    print(f"📦 주문번호: {new_order.id} | 총 결제금액: {new_order.totalAmount}원")
                    cart.clearCart() # 장바구니 비우기
                except ValueError as e:
                    print(e)

        # 3. 주문 및 배송 조회
        elif choice == "3":
            print("\n📦 [배송 및 주문 내역 조회]")
            if not orders:
                print("최근 주문 내역이 없습니다.")
                continue
                
            for order in orders:
                print(f"■ 주문번호: {order.id} (주문일시: {order.orderDate.strftime('%Y-%m-%d %H:%M:%S')})")
                for oi in order.orderItems:
                    print(f"   - {oi.product.name} x {oi.quantity}개")
                print(f"   💰 총 결제금액: {order.totalAmount}원")
                print(f"   🚚 배송 상태: [{order.delivery.status.value}] | 배송지: {order.delivery.address} | 송장번호: {order.delivery.trackingNo}")
                print("-" * 40)

        # 4. 리뷰 작성
        elif choice == "4":
            print("\n✍️ [리뷰 작성하기]")
            if not orders:
                print("❌ 상품을 구매한 내역이 있어야 리뷰를 남길 수 있습니다.")
                continue
                
            # 구매한 상품 리스트업
            purchased_products = {}
            for order in orders:
                for oi in order.orderItems:
                    purchased_products[oi.product.id] = oi.product
            
            print("최근 구매하신 상품 목록입니다:")
            for p_id, p in purchased_products.items():
                print(f" [{p_id}] {p.name}")
                
            try:
                target_id = int(input("리뷰를 작성할 상품 번호를 입력하세요: "))
                if target_id not in purchased_products:
                    print("❌ 구매 내역에 없는 상품입니다.")
                    continue
                
                rating = int(input("평점을 입력하세요 (1점 ~ 5점): "))
                if not (1 <= rating <= 5):
                    print("❌ 평점은 1에서 5 사이여야 합니다.")
                    continue
                    
                content = input("리뷰 내용을 작성해 주세요: ")
                
                new_review = Review(len(reviews) + 1, rating, content, current_user, purchased_products[target_id])
                reviews.append(new_review)
                print(f"⭐️ 리뷰가 등록되었습니다! (평점: {rating}점)")
            except ValueError:
                print("❌ 올바른 숫자를 입력해 주세요.")

        # 5. 관리자 모드 현황 파악
        elif choice == "5":
            print("\n👑 [관리자 전용 대시보드 - 현황 관리]")
            print("[1] 상품별 현재 재고 상황")
            for p in products:
                print(f"  - {p.name}: {p.stock}개 남음")
                
            print("\n[2] 누적 매출 현황")
            total_sales = sum(o.totalAmount for o in orders)
            print(f"  - 총 매출액: {total_sales}원")
            print(f"  - 총 주문 건수: {len(orders)}건")
            
            print("\n[3] 최신 리뷰 피드백")
            if not reviews:
                print("  - 등록된 고객 리뷰가 없습니다.")
            for r in reviews:
                print(f"  - [{r.product.name}] 평점: {r.rating} | 내용: {r.content} ({r.member.name}님)")

        # 0. 종료
        elif choice == "0":
            print("\n👋 이용해 주셔서 감사합니다. 쇼핑몰 프로그램을 종료합니다.")
            break
        else:
            print("❌ 잘못된 번호입니다. 0 ~ 5 사이의 숫자를 입력해 주세요.")


if __name__ == "__main__":
    run_shop_simulation()