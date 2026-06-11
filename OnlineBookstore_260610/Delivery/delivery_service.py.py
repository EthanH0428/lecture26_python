class DeliveryService:
    def __init__(self, delivery_dao):
        self.delivery_dao = delivery_dao

    def create_delivery(self, order_id, member_id, address):
        return self.delivery_dao.insert(order_id, member_id, address)

    def view_delivery_by_order(self, order_id):
        return self.delivery_dao.select_by_order_id(order_id)

    def view_member_deliveries(self, member_id):
        return self.delivery_dao.select_by_member_id(member_id)

    def change_status(self, delivery_id, status):
        return self.delivery_dao.update_status(delivery_id, status)