from model import Member, Product

class MemberDAO:
    def __init__(self):
        # PPT 더미 데이터 기준 초기화
        self._member_database = {
            "test": Member(1, "test", "1234", "김싸피", "SILVER")
        }

    def find_by_login_id(self, login_id: str) -> Member:
        return self._member_database.get(login_id)

class ProductDAO:
    def __init__(self):
        # PPT 구현 화면 기준 상품 데이터 구성
        self._products = [
            Product(1, "유기농 연어 사료 2kg", 35000, 10, "눈물 개선에 좋은 최고급 사료"),
            Product(2, "치석 제거 덴탈껌 30P", 12000, 20, "매일 즐겁게 하는 치아 관리"),
            Product(3, "고양이 캣닢 스크래쳐", 18000, 5, "스트레스 해소용 고밀도 스크래쳐")
        ]

    def find_all(self) -> list:
        return self._products

    def find_by_id(self, product_id: int) -> Product:
        for p in self._products:
            if p.id == product_id:
                return p
        return None