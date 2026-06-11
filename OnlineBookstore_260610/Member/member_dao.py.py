class MemberDAO:
    def __init__(self):
        # 메모리 데이터베이스 역할 (초기 관리자 계정 생성)
        self._members = {
            'admin': {
                'password': 'admin',
                'name': '관리자',
                'phone': '010-0000-0000',
                'email': 'admin@bookstore.com'
            }
        }

    def insert(self, member):
        if member.get_member_id() in self._members:
            return False
        self._members[member.get_member_id()] = {
            'password': member.get_password(),
            'name': member.get_name(),
            'phone': member.get_phone(),
            'email': member.get_email()
        }
        return True

    def select_by_id(self, member_id):
        data = self._members.get(member_id)
        if data:
            from Member.member import Member
            return Member(member_id, data['password'], data['name'], data['phone'], data['email'])
        return None

    def update_password(self, member_id, new_password):
        if member_id in self._members:
            self._members[member_id]['password'] = new_password
            return True
        return False

    def delete(self, member_id):
        if member_id in self._members:
            del self._members[member_id]
            return True
        return False

    def select_all(self):
        from Member.member import Member
        member_list = []
        for m_id, data in self._members.items():
            member_list.append(Member(m_id, data['password'], data['name'], data['phone'], data['email']))
        return member_list