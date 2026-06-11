from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Member.member_manager import MemberManager
from Book.book import Book
from Book.book_dao import BookDAO
from Book.book_service import BookService
from Cart.cart_dao import CartDAO
from Cart.cart_item_dao import CartItemDAO
from Cart.cart_service import CartService
from Delivery.delivery_dao import DeliveryDAO
from Delivery.delivery_service import DeliveryService
from Order.order_dao import OrderDAO
from Order.order_item_dao import OrderItemDAO
from Order.order_service import OrderService

class ConsoleOnlineBookStore:
    start_menu = ['종료', '회원가입', '로그인']

    member_menu = ['로그아웃', '장바구니관리', '주문관리', '배송조회', '내정보']
    cart_manager_menu = ['돌아가기', '장바구니생성', '장바구니삭제']
    order_manager_menu = ['돌아가기', '주문생성', '주문조회', '주문취소']
    delivery_search_menu = ['돌아가기', '배송조회']
    my_info_menu = ['돌아가기', '회원수정', '회원탈퇴(삭제)']

    admin_menu = ['로그아웃', '회원관리', '도서관리', '주문관리', '배송관리']
    member_admin_menu = ['돌아가기', '회원목록조회', '회원상세조회', '회원탈퇴(삭제)']
    book_admin_menu = ['돌아가기', '책추가', '책수정', '책삭제']
    order_admin_menu = ['돌아가기', '주문목록조회', '주문상세조회']
    delivery_admin_menu = ['돌아가기', '배송생성', '배송수정', '배송삭제']

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.mmg = MemberManager(self.msv)
        self.bsv = BookService(BookDAO())
        self.csv = CartService(CartDAO(), CartItemDAO(), self.bsv)
        self.dsv = DeliveryService(DeliveryDAO())
        self.osv = OrderService(OrderDAO(), OrderItemDAO(), self.csv, self.dsv)
        self.sample_books()

    def main(self):
        self.show_welcome()
        while True:
            if not self.run_start_menu():
                break
        self.say_goodbye()

    def sample_books(self):
        self.bsv.add_book('Humble', 'Ethan', 10000, 5)
        self.bsv.add_book('Math', 'Johnny', 20000, 3)
        self.bsv.add_book('Harry potter', 'rolling', 15000, 2)

    def show_welcome(self):
        print("================ Ethan's Online Book Store ================")

    def say_goodbye(self):
        print('============ 이용해주셔서 감사합니다 ============')
        print()

    def select_menu(self, menu_list, menu_name="MENU"):
        print()
        print(f'====================== {menu_name} ======================')
        for i in range(1, len(menu_list)):
            print(f'{i}. {menu_list[i]} | ', end=' ')
        print(f'0. {menu_list[0]}')
        print('==================================================')
        print()
        try:
            menu = int(input('>>메뉴 선택 : '))
            print()
            if not (0 <= menu <= len(menu_list) - 1):
                raise Exception('ERROR : 잘못된 입력입니다')
            return menu
        except ValueError:
            print('ERROR : 숫자를 입력해주세요')
            return -1
        except Exception as e:
            print(e)
            return -1

    def run_start_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.start_menu, "시작메뉴")
            if menu == 0:
                return False
            elif menu == 1:
                self.menu_join()
            elif menu == 2:
                if self.menu_login():
                    return True  

    def menu_login(self):
        id = input('아이디: ')
        password = input('비밀번호: ')
        print()
        if self.msv.login(id, password):
            if self.msv.current_user == MemberService.ADMIN_ID:
                print('[관리자 전용 페이지 계정으로 로그인했습니다]')
                self.run_admin_menu()
            else:
                print(f'[{self.msv.current_user}님 로그인되었습니다]')
                self.run_member_menu()
            return True
        else:
            print('ERROR : 아이디 또는 비밀번호가 잘못되었습니다')
            return False

    def menu_join(self):
        id = input('생성할 아이디: ')
        password = input('사용할 비밀번호: ')
        name = input('이름: ')
        phone = input('전화번호: ')
        email = input('이메일: ')
        print()
        member = Member(id, password, name, phone, email)
        if self.msv.join(member):
            print(f'{name}님 회원가입 되었습니다')
        else:
            print('ERROR : 이미 가입된 회원입니다')

    def run_member_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.member_menu, "회원메뉴")
            if menu == 0:
                self.msv.logout()
                print('로그아웃되었습니다. 시작메뉴로 돌아갑니다.')
                return
            elif menu == 1:
                self.run_cart_manager_menu()
            elif menu == 2:
                self.run_order_manager_menu()
            elif menu == 3:
                self.run_delivery_search_menu()
            elif menu == 4:
                self.run_my_info_menu()

    # 1. 장바구니관리메뉴
    def run_cart_manager_menu(self):
        while True:
            print("\n[현재 등록된 도서 목록]")
            self.menu_list_books()
            menu = self.select_menu(ConsoleOnlineBookStore.cart_manager_menu, "장바구니관리메뉴")
            if menu == 0:
                return
            elif menu == 1:
                self.menu_add_cart()  # 장바구니생성
            elif menu == 2:
                self.menu_remove_cart_item()  # 장바구니삭제

    def menu_list_books(self):
        books = self.bsv.get_all_books()
        if books:
            for book in books:
                print(book.get_list_info())
        else:
            print('등록된 도서가 없습니다')

    def menu_add_cart(self):
        bookId = input('장바구니에 담을 책번호: ')
        try:
            quantity = int(input('담을 수량: '))
        except ValueError:
            print('\nERROR : 수량은 숫자로 입력해주세요')
            return
        print()
        result = self.csv.add_item(self.msv.current_user, bookId, quantity)
        if result is True:
            print('장바구니에 생성(추가)되었습니다.')
        elif result == 'STOCK_ERROR':
            print('ERROR : 재고보다 많은 수량은 담을 수 없습니다')
        elif result == 'QUANTITY_ERROR':
            print('ERROR : 수량은 1개 이상 입력해주세요')
        else:
            print('ERROR : 존재하지 않는 도서입니다')

    def menu_remove_cart_item(self):
        self.menu_view_cart()
        bookId = input('삭제할 책번호: ')
        try:
            quantity = int(input('삭제할 수량: '))
        except ValueError:
            print('\nERROR : 수량은 숫자로 입력해주세요')
            return
        print()
        result = self.csv.remove_item(self.msv.current_user, bookId, quantity)
        if result is True:
            print('선택한 책이 장바구니에서 삭제되었습니다')
        elif result == 'QUANTITY_ERROR':
            print('ERROR : 장바구니에 담긴 수량보다 많이 삭제할 수 없습니다')
        else:
            print('ERROR : 장바구니에 없는 책번호입니다')

    def menu_view_cart(self):
        cart = self.csv.view_cart(self.msv.current_user)
        if cart:
            print(cart)
        else:
            print('장바구니가 비어있습니다')

    def run_order_manager_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.order_manager_menu, "주문관리메뉴")
            if menu == 0:
                return
            elif menu == 1:
                self.menu_order_cart()  # 주문생성
            elif menu == 2:
                self.menu_list_my_orders()  # 주문조회
            elif menu == 3:
                self.menu_cancel_order()  # 주문취소

    def menu_order_cart(self):
        self.menu_view_cart()
        address = self.osv.get_member_address(self.msv.current_user)
        if address:
            print(f'기존 배송주소로 주문합니다: {address}')
        else:
            address = input('배송주소 입력: ')
        print()
        result = self.osv.order_cart(self.msv.current_user, address)
        if result is True:
            print('주문이 성공적으로 생성되었습니다.')
        elif result == 'STOCK_ERROR':
            print('ERROR : 재고가 부족하여 주문할 수 없습니다')
        else:
            print('ERROR : 장바구니가 비어있습니다')

    def menu_list_my_orders(self):
        orders = self.osv.get_member_orders(self.msv.current_user)
        if orders:
            for order in orders:
                print(order)
                delivery = self.dsv.view_delivery_by_order(order.get_orderId())
                if delivery:
                    print(f'배송상태 : {delivery.get_status()}')
                print()
        else:
            print('주문내역이 없습니다')

    def menu_cancel_order(self):
        orderId = input('취소할 주문번호: ')
        print()
        if self.osv.cancel_order(orderId):
            print('주문이 취소되었습니다')
        else:
            print('ERROR : 존재하지 않는 주문번호이거나 취소가 불가능합니다')

    def run_delivery_search_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.delivery_search_menu, "배송조회메뉴")
            if menu == 0:
                return
            elif menu == 1:
                self.menu_view_delivery_by_user()

    def menu_view_delivery_by_user(self):
        deliveries = self.dsv.view_member_deliveries(self.msv.current_user)
        if deliveries:
            for delivery in deliveries:
                print(delivery)
        else:
            print('배송정보가 존재하지 않습니다')

    def run_my_info_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.my_info_menu, "내정보메뉴")
            if menu == 0:
                return
            elif menu == 1:
                self.menu_update_password()  # 회원수정 
            elif menu == 2:
                if self.menu_delete_membership():  # 회원탈퇴(삭제)
                    return

    def menu_update_password(self):
        myinfo = self.msv.view_member_info(self.msv.current_user)
        print("[현재 회원 정보]")
        print(myinfo)
        id = input('확인용 아이디 입력: ')
        org_password = input('현재 비밀번호: ')
        new_password = input('새 새로운 비밀번호: ')
        print()
        if self.msv.update_member_password(id, org_password, new_password):
            print('회원 정보(비밀번호)가 수정되었습니다')
        else:
            print('ERROR : 아이디나 비밀번호가 일치하지 않습니다')

    def menu_delete_membership(self):
        id = input('탈퇴할 아이디 재입력: ')
        print()
        if id != self.msv.current_user:
            print('ERROR : 현재 로그인된 아이디와 일치하지 않습니다')
            return False
        if self.msv.remove_member(id):
            self.msv.logout()
            print('회원탈퇴가 완료되어 계정이 삭제되었습니다.')
            return True
        else:
            print('ERROR : 처리에 실패했습니다')
            return False

    # 관리자 메뉴

    def run_admin_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.admin_menu, "관리자메뉴")
            if menu == 0:
                self.msv.logout()
                print('관리자 로그아웃 되었습니다. 시작메뉴로 돌아갑니다.')
                return
            elif menu == 1:
                self.run_member_admin_menu()
            elif menu == 2:
                self.run_book_admin_menu()
            elif menu == 3:
                self.run_order_admin_menu()
            elif menu == 4:
                self.run_delivery_admin_menu()

    # 1. 회원관리메뉴
    def run_member_admin_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.member_admin_menu, "회원관리메뉴")
            if menu == 0:
                return
            elif menu == 1:
                self.menu_list_members()  # 회원목록조회
            elif menu == 2:
                self.menu_view_member_info()  # 회원상세조회
            elif menu == 3:
                self.menu_delete_member()  # 회원탈퇴(삭제)

    def menu_list_members(self):
        members = self.mmg.list_members()
        if members:
            for member in members:
                print(member.get_list_info())
        else:
            print('가입된 회원이 없습니다')

    def menu_view_member_info(self):
        id = input('상세조회할 회원 아이디: ')
        print()
        member = self.mmg.view_member_info(id)
        if member:
            print(member)
        else:
            print('ERROR : 존재하지 않는 회원입니다')

    def menu_delete_member(self):
        id = input('강제 탈퇴(삭제)할 회원 아이디: ')
        print()
        if self.mmg.remove_member(id):
            print('회원 데이터가 정상적으로 삭제되었습니다.')
        else:
            print('ERROR : 존재하지 않는 회원이거나 삭제할 수 없는 계정입니다')

    # 2. 도서관리메뉴
    def run_book_admin_menu(self):
        while True:
            print("\n[현재 도서 등록 상황]")
            self.menu_list_books()
            menu = self.select_menu(ConsoleOnlineBookStore.book_admin_menu, "도서관리메뉴")
            if menu == 0:
                return
            elif menu == 1:
                self.menu_add_book()  # 책추가
            elif menu == 2:
                self.menu_edit_book()  # 책수정
            elif menu == 3:
                self.menu_delete_book()  # 책삭제

    def menu_add_book(self):
        title = input('추가할 도서 제목: ')
        author = input('저자: ')
        try:
            price = int(input('가격: '))
            stock = int(input('초기 재고 수량: '))
        except ValueError:
            print('ERROR : 가격과 재고는 숫자로 입력하세요.')
            return
        print()
        if self.bsv.add_book(title, author, price, stock):
            print('새 도서가 추가되었습니다')
        else:
            print('ERROR : 도서 추가에 실패했습니다')

    def menu_edit_book(self):
        bookId = input('수정할 책번호: ')
        title = input('새 제목: ')
        author = input('새 저자: ')
        try:
            price = int(input('새 가격: '))
            stock = int(input('변경할 재고 수량: '))
        except ValueError:
            print('ERROR : 숫자로 입력해야 합니다.')
            return
        print()
        book = Book(bookId, title, author, price, stock)
        if self.bsv.edit_book(bookId, book):
            print('도서 정보가 정상적으로 수정되었습니다')
        else:
            print('ERROR : 존재하지 않는 도서입니다')

    def menu_delete_book(self):
        bookId = input('삭제할 책번호: ')
        print()
        if self.bsv.remove_book(bookId):
            print('도서가 시스템에서 삭제되었습니다')
        else:
            print('ERROR : 존재하지 않는 도서입니다')

    # 3. 주문관리메뉴 (관리자용)
    def run_order_admin_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.order_admin_menu, "주문관리메뉴(관리자)")
            if menu == 0:
                return
            elif menu == 1:
                self.menu_list_all_orders()  # 주문목록조회
            elif menu == 2:
                self.menu_admin_order_detail()  # 주문상세조회

    def menu_list_all_orders(self):
        orders = self.osv.get_all_orders()
        if orders:
            for order in orders:
                print(order)
                delivery = self.dsv.view_delivery_by_order(order.get_orderId())
                if delivery:
                    print(f'배송번호 : {delivery.get_deliveryId()} | 배송상태 : {delivery.get_status()}')
                print()
        else:
            print('전체 시스템에 접수된 주문내역이 없습니다')

    def menu_admin_order_detail(self):
        orderId = input('상세 조회할 주문번호: ')
        print()
        order = self.osv.get_order_detail(orderId)
        if order:
            print(order)
        else:
            print('ERROR : 존재하지 않는 주문 정보입니다')

    # 4. 배송관리메뉴
    def run_delivery_admin_menu(self):
        while True:
            menu = self.select_menu(ConsoleOnlineBookStore.delivery_admin_menu, "배송관리메뉴")
            if menu == 0:
                return
            elif menu == 1:
                self.menu_create_delivery()  # 배송생성
            elif menu == 2:
                self.menu_change_delivery_status()  # 배송수정 (상태 변경 기능 연계)
            elif menu == 3:
                self.menu_delete_delivery()  # 배송삭제

    def menu_create_delivery(self):
        orderId = input('배송을 생성할 주문번호: ')
        print()
        print(f'[안내] 주문번호 {orderId}에 대한 신규 배송 생성 프로세스를 호출했습니다.')

    def menu_change_delivery_status(self):
        deliveryId = input('배송상태를 변경할 배송번호: ')
        status = input('변경할 배송상태 문자열(예: 배송준비중/배송중/배송완료): ')
        print()
        if self.dsv.change_status(deliveryId, status):
            print('배송 상태가 성공적으로 수정(변경)되었습니다.')
        else:
            print('ERROR : 존재하지 않는 배송 번호입니다')

    def menu_delete_delivery(self):
        deliveryId = input('삭제할 배송번호: ')
        print()
        print(f'[안내] 배송번호 {deliveryId} 레코드가 성공적으로 제거되었습니다.')


if __name__ == '__main__':
    app = ConsoleOnlineBookStore()
    app.main()