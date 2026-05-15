class Member:
    """회원 정보를 담는 클래스"""
    def __init__(self, member_id, login_id, password, name, phone, address):
        self.member_id = member_id
        self.login_id = login_id
        self.password = password
        self.name = name
        self.phone = phone
        self.address = address

    def __str__(self):
        return f"[{self.member_id}] ID: {self.login_id} | 이름: {self.name} | 전화: {self.phone} | 주소: {self.address}"


class MemberService:
    """회원 관리 기능을 수행하는 클래스"""
    def __init__(self):
        self.members = []
        self.current_id = 1

    def join(self):
        """회원 가입"""
        print("\n--- 회원 가입 ---")
        login_id = input("아이디: ").strip()
        if not login_id:
            print("오류: 아이디는 필수 입력 사항입니다.")
            return
            
        password = input("비밀번호: ")
        name = input("이름: ")
        phone = input("전화번호: ")
        address = input("주소: ")
        
        new_member = Member(self.current_id, login_id, password, name, phone, address)
        self.members.append(new_member)
        self.current_id += 1
        print(f"회원 가입이 완료되었습니다. (회원번호: {self.current_id - 1})")

    def show_list(self):
        """회원 목록 조회"""
        print("\n--- 회원 목록 ---")
        if not self.members:
            print("등록된 회원이 없습니다.")
            return
        for member in self.members:
            print(member)

    def show_detail(self):
        """회원 상세 정보 (예외 처리 추가)"""
        print("\n--- 회원 상세 정보 ---")
        try:
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
            print("해당 번호의 회원을 찾을 수 없습니다.")
        except ValueError:
            print("오류: 회원번호는 숫자만 입력 가능합니다.")

    def update_member(self):
        """회원 정보 수정 (예외 처리 추가)"""
        print("\n--- 회원 정보 수정 ---")
        try:
            target_id = int(input("수정할 회원번호를 입력하세요: "))
            for member in self.members:
                if member.member_id == target_id:
                    member.password = input("새 비밀번호: ")
                    member.phone = input("새 전화번호: ")
                    member.address = input("새 주소: ")
                    print("수정이 완료되었습니다.")
                    return
            print("해당 번호의 회원을 찾을 수 없습니다.")
        except ValueError:
            print("오류: 회원번호는 숫자만 입력 가능합니다.")

    def delete_member(self):
        """회원 탈퇴 (예외 처리 추가)"""
        print("\n--- 회원 탈퇴 ---")
        try:
            target_id = int(input("탈퇴할 회원번호를 입력하세요: "))
            for i, member in enumerate(self.members):
                if member.member_id == target_id:
                    del self.members[i]
                    print("탈퇴 처리가 완료되었습니다.")
                    return
            print("해당 번호의 회원을 찾을 수 없습니다.")
        except ValueError:
            print("오류: 회원번호는 숫자만 입력 가능합니다.")


def main():
    """메인 UI 및 로직 제어"""
    service = MemberService()
    
    while True:
        print("\n===== 회원 관리 프로그램 =====")
        print("1. 회원가입 | 2. 회원목록 | 3. 상세정보 | 4. 정보수정 | 5. 회원탈퇴 | 0. 종료")
        choice = input("메뉴 선택: ")

        try:
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
                print("잘못된 메뉴 선택입니다. (0~5 사이의 숫자를 입력하세요)")
        except Exception as e:
            # 예상치 못한 시스템 에러 발생 시 프로그램 종료 방지
            print(f"알 수 없는 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()