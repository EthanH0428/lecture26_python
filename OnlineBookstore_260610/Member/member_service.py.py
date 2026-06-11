class MemberService:
    ADMIN_ID = 'admin'

    def __init__(self, member_dao):
        self.member_dao = member_dao
        self.current_user = None

    def login(self, member_id, password):
        member = self.member_dao.select_by_id(member_id)
        if member and member.get_password() == password:
            self.current_user = member_id
            return True
        return False

    def logout(self):
        self.current_user = None

    def join(self, member):
        return self.member_dao.insert(member)

    def view_member_info(self, member_id):
        return self.member_dao.select_by_id(member_id)

    def update_member_password(self, member_id, org_password, new_password):
        member = self.member_dao.select_by_id(member_id)
        if member and member.get_password() == org_password:
            return self.member_dao.update_password(member_id, new_password)
        return False

    def remove_member(self, member_id):
        if member_id == self.ADMIN_ID:
            return False
        return self.member_dao.delete(member_id)