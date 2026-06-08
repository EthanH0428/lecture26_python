from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Account.account import Account
from Account.account_dao import AccountDAO
from Account.account_service import AccountService

class ConsoleBank:
    start_menu = ['종료', '로그인', '회원가입']
    banking_menu = ['로그아웃', '계좌목록', '입금', '출금', '계좌생성', '계좌해지', '내 정보']
    member_myinfo_menu = ['돌아가기', '비밀번호 수정', '회원탈퇴']
    admin_menu = ['로그아웃', '회원관리', '계좌관리']
    admin_account_menu = ['돌아가기', '전체계좌목록', '회원별계좌목록', '회원강퇴']
    admin_member_menu = ['돌아가기', '회원목록', '회원정보조회']

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.asv = AccountService(AccountDAO())

    def main(self):
        self.show_welcome()
        while True:
            try:
                menu = self.select_menu(ConsoleBank.start_menu)
                if menu == 0: 
                    break
                elif menu == 1:
                    self.menu_login()
                elif menu == 2:
                    self.menu_join()
            except Exception as e:
                if str(e) == "FORCE_LOGOUT":
                    continue
                else:
                    print(f"오류가 발생했습니다: {e}")
                    break
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

    def menu_join(self):
        print('\n>>>>> 회원가입 <<<<<<')
        member_id = input('>> 아이디 : ')
        password = input('>> 비밀번호 : ')
        name = input('>> 이름 : ')
        
        new_member = Member(member_id, password, name)
        if self.msv.join(new_member): 
            print(f'회원 {name}님의 가입이 완료되었습니다.')
        else:
            print('이미 존재하는 아이디이거나 회원가입을 할 수 없습니다.')

    def menu_login(self):
        print('\n>>>>> 로그인 <<<<<<')
        member_id = input('>> 아이디 : ')
        password = input('>> 비밀번호 : ')
        
        if self.msv.login(member_id, password): 
            if self.msv.current_user == MemberService.ADMIN_ID:
                print('\n관리자 계정으로 로그인했습니다.')
                self.run_admin_menu()
            else:
                print(f'\n로그인 성공했습니다.')
                self.run_banking_menu()
        else:
            print('아이디 또는 비밀번호가 틀렸습니다.')

    def menu_logout(self):
        print('\n>>>>> 로그아웃 <<<<<<')
        self.msv.logout() 
        print('로그아웃 되었습니다.')

    def run_banking_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.banking_menu)
            if menu == 0: 
                self.menu_logout()
                break
            elif menu == 1: self.menu_list_my_accounts()
            elif menu == 2: self.menu_deposit()
            elif menu == 3: self.menu_withdraw()
            elif menu == 4: self.menu_create_account()
            elif menu == 5: self.menu_delete_account()
            elif menu == 6: self.menu_myinfo()

    def menu_list_my_accounts(self):
        print('\n>>>>> 계좌목록 조회 <<<<<<')
        self.list_members_accounts(self.msv.current_user)

    def list_members_accounts(self, user):
        accounts = self.asv.get_accounts_by_member(user) 
        if accounts:
            for acc in accounts:
                print(f'계좌번호: {acc.account_no} | 잔액: {acc.balance:,}원')
        else:
            print('보유하신 계좌가 없습니다.')

    def menu_deposit(self):
        print('\n>>>>> 입금 <<<<<<')
        self.list_members_accounts(self.msv.current_user)
        account_no = input('>> 계좌번호 : ')
        amount = int(input('입금액 : '))
        if self.asv.deposit(account_no, amount):
            print(f'계좌번호 {account_no}에 {amount:,}원을 입금했습니다.')
            balance = self.asv.get_account_balance(account_no)
            if balance >= 0:
                print(f'잔액 : {balance:,}')
        else:
            print('입금을 할 수 없습니다.')

    def menu_withdraw(self):
        print('\n>>>>> 출금 <<<<<<')
        self.list_members_accounts(self.msv.current_user)
        account_no = input('>> 계좌번호 : ')
        amount = int(input('출금액 : '))
        
        if self.asv.withdraw(account_no, amount):
            print(f'계좌번호 {account_no}에서 {amount:,}원을 출금했습니다.')
            balance = self.asv.get_account_balance(account_no)
            print(f'잔액 : {balance:,}')
        else:
            print('잔액이 부족하거나 출금을 할 수 없습니다.')

    def menu_create_account(self):
        print('\n>>>>> 계좌생성 <<<<<<')
        account_no = input('>> 신규 계좌번호 : ')
        amount = int(input('초기 입금액 : '))
        
        new_account = Account(account_no, self.msv.current_user, amount)
        if self.asv.create_account(new_account):
            print(f'계좌번호 {account_no}가 성공적으로 개설되었습니다.')
        else:
            print('이미 존재하는 계좌번호이거나 생성할 수 없습니다.')

    def menu_delete_account(self):
        print('\n>>>>> 계좌해지 <<<<<<')
        account_no = input('>> 해지할 계좌번호 : ')
        if self.asv.delete_account(account_no):
            print(f'계좌번호 {account_no}가 정상적으로 해지되었습니다.')
        else:
            print('계좌를 해지할 수 없습니다. 번호를 확인해주세요.')
    
    def menu_myinfo(self):
        self.run_my_info_menu()

    def run_my_info_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.member_myinfo_menu)
            if menu == 0: 
                break                
            elif menu == 1: self.menu_update_password()
            elif menu == 2: self.menu_delete_membership()

    def menu_update_password(self):
        print('\n>>>>> 비밀번호 수정 <<<<<<')
        old_pw = input('>> 현재 비밀번호 : ')
        new_pw = input('>> 새로운 비밀번호 : ')
        
        if self.msv.update_member_password(self.msv.current_user, old_pw, new_pw):
            print('비밀번호가 변경되었습니다.')
        else:
            print('현재 비밀번호가 일치하지 않거나 본인 계정이 아닙니다.')

    def menu_delete_membership(self):
        print('\n>>>>> 회원탈퇴 <<<<<<')
        pw = input('>> 본인확인 비밀번호 : ')
        
        member = self.msv.view_member_info(self.msv.current_user)
        if member and member.get_password() == pw:
            if self.msv.remove_member(self.msv.current_user):
                print('회원탈퇴가 처리되었습니다. 그동안 이용해 주셔서 감사합니다.')
                self.msv.logout()
                raise Exception("FORCE_LOGOUT")
        else:
            print('비밀번호가 올바르지 않습니다.')

    # =========================================================================
    # 관리자 영역
    # =========================================================================

    def run_admin_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_menu)
            if menu == 0:
                self.menu_logout()   
                break
            elif menu == 1: self.menu_manage_members()  
            elif menu == 2: self.menu_manage_accounts() 

    def menu_manage_members(self): self.run_admin_member_menu()
    def menu_manage_accounts(self): self.run_admin_account_menu()

    def run_admin_account_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_account_menu)
            if menu == 0:
                break                
            elif menu == 1: self.menu_list_all_accounts()
            elif menu == 2: self.menu_list_member_accounts()
            elif menu == 3: self.menu_delete_member() # 회원 강퇴 메뉴 연동

    def menu_list_all_accounts(self):
        print('\n>>>>> 전체계좌목록 <<<<<<')
        accounts = self.asv.get_all_accounts()
        for acc in accounts:
            print(f'소유자: {acc.member_id} | 계좌: {acc.account_no} | 잔액: {acc.balance:,}원')

    def menu_list_member_accounts(self):
        print('\n>>>>> 회원별계좌목록 <<<<<<')
        target_user = input('>> 조회할 회원 ID : ')
        self.list_members_accounts(target_user)

    def run_admin_member_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.admin_member_menu)
            if menu == 0:
                break                
            elif menu == 1: self.menu_list_members()
            elif menu == 2: self.menu_view_member_info()

    def menu_list_members(self):
        print('\n>>>>> 회원목록 <<<<<<')
        members = self.msv.list_members()
        for m in members:
            print(f'ID: {m.get_id()} | 이름: {m.get_name()}')

    def menu_view_member_info(self):
        print('\n>>>>> 회원정보조회 <<<<<<')
        target_user = input('>> 조회할 회원 ID : ')
        m = self.msv.view_member_info(target_user)
        if m:
            print(f'ID: {m.get_id()}\n이름: {m.get_name()}')
        else:
            print('존재하지 않는 회원입니다.')

    def menu_delete_member(self):
        print('\n>>>>> 회원강퇴 <<<<<<')
        target_user = input('>> 강퇴할 회원 ID : ')
        
        if target_user == MemberService.ADMIN_ID:
            print("관리자 계정은 강퇴할 수 없습니다.")
            return

        if self.msv.remove_member(target_user):
            # 회원이 강퇴되면 해당 회원의 계좌도 함께 삭제 처리
            self.asv.delete_all_accounts_of_member(target_user) 
            print(f'회원 {target_user}님이 강제 탈퇴 처리되었습니다.')
        else:
            print('회원을 찾을 수 없거나 강퇴에 실패했습니다.')


if __name__ == '__main__':
    app = ConsoleBank()
    app.main()