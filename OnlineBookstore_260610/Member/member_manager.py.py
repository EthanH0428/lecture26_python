class MemberManager:
    def __init__(self, member_service):
        self.member_service = member_service

    def list_members(self):
        # 관리자 계정을 제외한 일반 회원 목록 반환
        all_members = self.member_service.member_dao.select_all()
        return [m for m in all_members if m.get_member_id() != 'admin']

    def view_member_info(self, member_id):
        return self.member_service.view_member_info(member_id)

    def remove_member(self, member_id):
        return self.member_service.remove_member(member_id)