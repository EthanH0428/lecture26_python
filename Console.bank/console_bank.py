from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Account.account import Account
from Account.account_dao import AccountDAO
from Account.account_service import AccountService

class ConsoleBank:
    start_menu = ['종료', '로그인', '회원가입']
    banking_menu = ['로그아웃', '계좌조회', '내정보관리']
    member_myinfo_menu = ['이전메뉴', '내정보보기', '비밀번호변경']

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.asv = AccountService(AccountDAO())

    def main(self):
        self.show_welcome()
        while True:
            menu = self.select_menu(ConsoleBank.start_menu)
            if menu == 0: 
                break
            elif menu == 1:
                self.menu_login()
            elif menu == 2:
                self.menu_join()
        self.say_goodbye()

    def show_welcome(self):
        print('======== Ethan Console Bank ============')

    def say_goodbye(self):
        print('>> Ethan Console Bank를 이용해 주셔서 감사합니다.')

    def select_menu(self, menu_list):
        print("\n" + "=" * 20)
        for i in range(len(menu_list)):
            print(f"{i}. {menu_list[i]}")
        print("=" * 20)
        
        return int(input("원하시는 메뉴 번호: "))


    def menu_login(self):
        print("로그인 되었습니다.")
        self.run_banking_menu()

    def menu_join(self):
        print("회원가입 페이지입니다.")

    def run_banking_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.banking_menu)
            if menu == 0: 
                print("로그아웃 되었습니다.")
                break
            elif menu == 1:
                print("계좌 리스트 조회 중...")
            elif menu == 2:
                self.run_my_info_menu()

    def run_my_info_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.member_myinfo_menu)
            if menu == 0: 
                break
            elif menu == 1:
                print("내 정보 보기")
            elif menu == 2:
                print("비밀번호 변경")


if __name__ == '__main__':
    app = ConsoleBank()
    app.main()