class Member:
    """회원 정보를 담는 클래스"""
    def __init__(self, member_id, login_id, password, name, phone, address):
        self.member_id = member_id  # 회원번호
        self.login_id = login_id    # 아이디
        self.password = password    # 비밀번호
        self.name = name            # 이름
        self.phone = phone          # 전화번호
        self.address = address      # 주소

    def __str__(self):
        return f"[{self.member_id}] ID: {self.login_id} | 이름: {self.name} | 전화: {self.phone} | 주소: {self.address}"


class MemberService:
    """회원 관리 기능을 수행하는 클래스"""
    def __init__(self):
        # 회원 객체들을 리스트로 관리
        self.members = []
        self.current_id = 1

    def join(self):
        """회원 가입"""
        print("\n--- 회원 가입 ---")
        login_id = input("아이디: ")
        password = input("비밀번호: ")
        name = input("이름: ")
        phone = input("전화번호: ")
        address = input("주소: ")
        
        new_member = Member(self.current_id, login_id, password, name, phone, address)
        self.members.append(new_member)
        self.current_id += 1
        print("회원 가입이 완료되었습니다.")

    def show_list(self):
        """회원 목록 조회"""
        print("\n--- 회원 목록 ---")
        if not self.members:
            print("등록된 회원이 없습니다.")
            return
        for member in self.members:
            print(member)

    def show_detail(self):
        """회원 상세 정보"""
        print("\n--- 회원 상세 정보 ---")
        target_id = int(input("조회할 회원번호를 입력하세요: "))
        for member in self.members:
            if member.member_id == target_id:
                print(f"회원번호: {member.member_id}")
                print(f"아이디: {member.login_id}")
                print(f"비밀번호: {member.password}")
                print(f"이름: {member.name}")
                print(f"전화번호: {member.phone}")
                print(f"주소: {member.address}")
                return
        print("해당 회원을 찾을 수 없습니다.")

    def update_member(self):
        """회원 정보 수정"""
        print("\n--- 회원 정보 수정 ---")
        target_id = int(input("수정할 회원번호를 입력하세요: "))
        for member in self.members:
            if member.member_id == target_id:
                member.password = input("새 비밀번호: ")
                member.phone = input("새 전화번호: ")
                member.address = input("새 주소: ")
                print("수정이 완료되었습니다.")
                return
        print("해당 회원을 찾을 수 없습니다.")

    def delete_member(self):
        """회원 탈퇴"""
        print("\n--- 회원 탈퇴 ---")
        target_id = int(input("탈퇴할 회원번호를 입력하세요: "))
        for i, member in enumerate(self.members):
            if member.member_id == target_id:
                del self.members[i]
                print("탈퇴 처리가 완료되었습니다.")
                return
        print("해당 회원을 찾을 수 없습니다.")


def main():
    """메인 UI 및 로직 제어"""
    service = MemberService()
    
    while True:
        print("\n===== 회원 관리 프로그램 =====")
        print("1. 회원가입")
        print("2. 회원목록")
        print("3. 상세정보")
        print("4. 정보수정")
        print("5. 회원탈퇴")
        print("0. 종료")
        choice = input("메뉴 선택: ")

        if choice == '1':
            service.join()
        elif choice == '2':
            service.show_list()
        elif choice == '3':
            service.show_detail()
        elif choice == '4':
            service.update_member()
        elif choice == '5':
            service.delete_member()
        elif choice == '0':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    main()