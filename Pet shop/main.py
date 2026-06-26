import sys
from service import ShopService, AdminService

def main():
    shop_service = ShopService()
    admin_service = AdminService(shop_service)

    print("=================================================")
    print("🐾 안녕하세요! 'Ethan의 반려용품 온라인 숍'에 오신 것을 환영합니다.")
    print("Welcome to Ethans Pet Shop!!")
    print("=================================================")
    
    # 1. 로그인 프로세스
    print("🔒 [로그인 화면]")
    login_id = input("- 아이디 입력: ").strip()
    password = input("- 비밀번호 입력: ").strip()

    if not shop_service.login(login_id, password):
        print("❌ 로그인 실패! 프로그램을 종료합니다.")
        sys.exit()

    user = shop_service.logined_member
    print(f"\n🎉 로그인 성공! {user.name} 님 반갑습니다. (등급: {user.grade})")

    # 2. 메인 메뉴 루프
    while True:
        print("\n==================== [메인 메뉴] ====================")
        print("1. 상품 목록 조회 및 담기 (상품 / 장바구니 메뉴)")
        print("2. 장바구니 확인 및 주문하기 (장바구니 / 주문 메뉴)")
        print("3. 주문 내역 및 배송 조회 (주문·배송 / 마이페이지 메뉴)")
        print("4. 구매 상품 리뷰 작성하기 (상품 / 마이페이지 메뉴)")
        print("5. [관리자 모드] 재고 및 매출 현황 확인")
        print("0. 쇼핑몰 종료")
        print("=================================================")
        
        try:
            menu = int(input("👉 원하시는 메뉴 번호를 입력하세요: "))
        except ValueError:
            print("숫자만 입력해 주세요.")
            continue

        if menu == 0:
            print("\n👋 이용해 주셔서 감사합니다. 쇼핑몰 프로그램을 종료합니다.")
            break
        elif menu == 1:
            handle_product_list(shop_service)
        elif menu == 2:
            handle_cart_and_order(shop_service)
        elif menu == 3:
            handle_order_history(shop_service)
        elif menu == 4:
            handle_review()
        elif menu == 5:
            handle_admin_dashboard(shop_service, admin_service)
        else:
            print("잘못된 메뉴 번호입니다.")

def handle_product_list(shop_service):
    print("\n🛒 [상품 목록]")
    products = shop_service.get_product_list()
    for p in products:
        print(f"[{p.id}] {p.name} | 가격: {p.price}원 | 재고: {p.stock}개 남음")
        print(f"    설명: {p.description}")
        
    try:
        p_id = int(input("\n장바구니에 담을 상품의 번호를 입력하세요 (취소하려면 0): "))
        if p_id == 0: return
        qty = int(input("상품을 몇 개 담으시겠습니까?: "))
        
        shop_service.add_to_cart(p_id, qty)
        target_product = shop_service.product_dao.find_by_id(p_id)
        print(f"🛒 '{target_product.name}' {qty}개가 장바구니에 담겼습니다.")
    except ValueError as e:
        print(f"❌ 입력 오류 또는 {e}")

def handle_cart_and_order(shop_service):
    cart = shop_service.cart
    print("\n💼 [나의 장바구니]")
    if not cart.items:
        print("장바구니가 비어 있습니다.")
        return
        
    for item in cart.items:
        print(f"- {item.product.name} : {item.quantity}개 = {item.get_subtotal()}원")
    print(f"💰 총 예상 결제 금액: {cart.get_total_price()}원")

    ans = input("\n💳 현재 장바구니 상태로 주문을 진행하시겠습니까? (Y/N): ").strip().upper()
    if ans == "Y":
        try:
            order = shop_service.create_order()
            print("\n✅ 주문 및 결제가 완료되었습니다!")
            print(f"📄 주문번호: {order.order_no} | 총 결제금액: {order.total_amount}원")
        except ValueError as e:
            print(f"❌ 주문 실패: {e}")

def handle_order_history(shop_service):
    print("\n📦 [배송 및 주문 내역 조회]")
    if not shop_service.orders:
        print("주문 내역이 없습니다.")
        return
        
    for o in shop_service.orders:
        print(f"■ 주문번호: {o.order_no}")
        for item in o.order_items:
            print(f"  - {item.product.name} x {item.quantity}개")
        print(f"  💰 총 결제금액: {o.total_amount}원")
        print(f"  🚚 배송 상태: [{o.delivery_status}] | 송장번호: {o.tracking_no}")

def handle_review():
    print("\n✍️ [리뷰 작성하기]")
    print("최근 구매하신 상품 목록입니다:")
    print("[3] 고양이 캣닢 스크래쳐")
    try:
        _ = int(input("리뷰를 작성할 상품 번호를 입력하세요: "))
        score = int(input("평점을 입력하세요 (1점 ~ 5점): "))
        _ = input("리뷰 내용을 작성해 주세요: ")
        print(f"⭐ 리뷰가 등록되었습니다! (평점: {score}점)")
    except ValueError:
        print("올바른 값을 입력해 주세요.")

def handle_admin_dashboard(shop_service, admin_service):
    print("\n👑 [관리자 전용 대시보드 - 현황 관리]")
    print("1] 상품별 현재 재고 상황")
    for p in shop_service.get_product_list():
        print(f"  - {p.name}: {p.stock}개 남음")
    print("\n2] 누적 매출 현황")
    print(f"  - 총 매출액: {admin_service.get_total_sales()}원")
    print(f"  - 총 주문 건수: {admin_service.get_total_order_count()}건")
    print("\n3] 최신 리뷰 피드백")
    print("  - 등록된 고객 리뷰가 없습니다.")

if __name__ == "__main__":
    main()