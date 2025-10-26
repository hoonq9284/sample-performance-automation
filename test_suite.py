import cmd
import requests
import random

# 전체 유저 수
_total_user_count = 0

# 유저 목록
_user_names = [
    "홍길동", "김민영", "이재현", "박소연", "최민석",
    "윤태우", "강나현", "장동민", "한지우", "오성훈",
    "임서윤", "서준호", "권예린", "배지수", "남건우",
    "신애리", "류동하", "하유진", "고수환"
]

# 유저 목록과 유저 ID 매핑 dict
_username_map = {
    "홍길동": "gildong_hong",
    "김민영": "minyoung_kim",
    "이재현": "jaehyun_lee",
    "박소연": "soyeon_park",
    "최민석": "minseok_choi",
    "윤태우": "taewoo_yoon",
    "강나현": "nahyun_kang",
    "장동민": "dongmin_jang",
    "한지우": "jiwoo_han",
    "오성훈": "sunghoon_oh",
    "임서윤": "seoyun_lim",
    "서준호": "junho_seo",
    "권예린": "yerin_kwon",
    "배지수": "jisoo_bae",
    "남건우": "gunwoo_nam",
    "신애리": "aeri_shin",
    "류동하": "dongha_ryu",
    "하유진": "yujin_ha",
    "고수환": "suhwan_ko"
}

# 각 항목 전역 변수
_name = lambda: _user_names[_total_user_count % len(_user_names)]
_username = lambda: _username_map[_name()]
_email = lambda: f"{_username()}@test.com"
_phone = lambda: "010-" + "".join(str(random.randint(0,9)) for _ in range(4)) + "-" + "".join(str(random.randint(0,9)) for _ in range(4))
_website = lambda: f"https://{_username()}.com"
_zipcode = lambda: random.randint(10000, 99999)


def get_request(url):
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")

def post_request(url, data):
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")

def delete_request(url):
    try:
        response = requests.delete(url)
        print(f"Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")

def get_user():
    url = "http://localhost:8000/users"
    get_request(url)

def create_user(count):
    global _total_user_count
    url = "http://localhost:8000/users"
    for i in range(count):
        data = {
            "name": _name(),
            "username": _username(),
            "email": _email(),
            "phone": _phone(),
            "website": _website(),
            "province": "경기도",
            "city": "성남시",
            "district": "분당구",
            "street": "대왕판교로 1234",
            "zipcode": _zipcode()
        }
        post_request(url, data)
        _total_user_count += 1
    print(f"전체 {_total_user_count}명의 유저가 추가되었습니다.")

def delete_user(count):
    global _total_user_count
    if count > _total_user_count:
        print("등록된 유저가 많지 않습니다.")
        count = _total_user_count
    for i in range(count):
        user_id = _total_user_count
        url = f"http://localhost:8000/users/{user_id}"
        delete_request(url)
        _total_user_count = _total_user_count - 1
    print(f"전체 {_total_user_count}명의 유저가 남아 있습니다.")

def delete_all_user():
    try:
        response = requests.get("http://localhost:8000/users")
        if response.status_code == 200:
            users = response.json()
            for user in users:
                user_id = user["id"]
                url = f"http://localhost:8000/users/{user_id}"
                delete_request(url)
    except requests.exceptions.RequestException as e:
        print(f"전체 유저 삭제 중 오류: {e}")


class APIShell(cmd.Cmd):
    intro = "FastAPI를 이용한 사용자 부하 테스트입니다. 'help' 를 입력하시면 도움말을 볼 수 있습니다."
    prompt = "(명령어 입력) "
    initialize = False

    def default(self, line):
        """정의되지 않은 명령어 사용 시"""
        if line.strip().upper() == "EOF":
            print("입력이 종료되었습니다. 프로그램을 종료합니다.")
            return True
        print(f"알 수 없는 명령어입니다. '{line}'")
        print("사용 가능한 명령어를 확인하려면 'help'를 입력하세요.")

    def do_help(self, arg):
        """도움말을 표시합니다."""
        print("사용 가능한 명령어:")
        print(" help - 명령어 사용 관련 도움말을 출력합니다.")
        print(" init - 프로그램을 초기화하여 사용 가능한 상태로 만듭니다.")
        print(" list - 현재 추가된 전체 유저 데이터를 조회합니다.")
        print(" add1 - 유저를 1명 추가합니다.")
        print(" add3 - 유저를 연속으로 3명 추가합니다.")
        print(" add10 - 유저를 연속으로 10명 추가합니다.")
        print(" del1 - 마지막으로 추가한 유저를 1명 삭제합니다.")
        print(" del3 - 마지막으로 추가한 유저를 연속으로 3명 삭제합니다.")
        print(" del10 - 마지막으로 추가한 유저를 연속으로 10명 삭제합니다.")

    def do_init(self, arg):
        """프로그램 초기화"""
        global _total_user_count
        print("프로그램 및 유저 수를 초기화합니다.")
        delete_all_user()
        _total_user_count = 0
        self.initialize = True
        print(f"프로그램 및 유저 수를 초기화했습니다. | 현재 유저 수: {_total_user_count}")

    def do_list(self, arg):
        """유저 전체 조회"""
        if not self.initialize:
            print("프로그램이 초기화되지 않았습니다. init 명령어를 사용하세요.")
            return
        print("유저를 조회합니다.")
        get_user()
        print(f"전체 유저 데이터를 조회하였습니다. | 현재 유저 수: {_total_user_count}명")

    def do_add1(self, arg):
        """유저 1명 추가"""
        if not self.initialize:
            print("프로그램이 초기화되지 않았습니다. init 명령어를 사용하세요.")
            return
        print("유저를 1명 추가합니다.")
        create_user(1)
        print(f"유저를 1명 추가했습니다. | 현재 유저 수: {_total_user_count}명")

    def do_add3(self, arg):
        """유저 3명 추가"""
        if not self.initialize:
            print("프로그램이 초기화되지 않았습니다. init 명령어를 사용하세요.")
            return
        print("유저를 3명 추가합니다.")
        create_user(3)
        print(f"유저를 3명 추가했습니다. | 현재 유저 수: {_total_user_count}명")

    def do_add10(self, arg):
        """유저 10명 추가"""
        if not self.initialize:
            print("프로그램이 초기화되지 않았습니다. init 명령어를 사용하세요.")
            return
        print("유저를 10명 추가합니다.")
        create_user(10)
        print(f"유저를 10명 추가했습니다. | 현재 유저 수: {_total_user_count}명")

    def do_del1(self, arg):
        """유저 1명 삭제"""
        if not self.initialize:
            print("프로그램이 초기화되지 않았습니다. init 명령어를 사용하세요.")
            return
        print("유저를 1명 삭제합니다.")
        delete_user(1)
        print(f"유저를 1명 삭제하였습니다. | 현재 유저 수: {_total_user_count}명")

    def do_del3(self, arg):
        """유저 3명 삭제"""
        if not self.initialize:
            print("프로그램이 초기화되지 않았습니다. init 명령어를 사용하세요.")
            return
        print("유저를 3명 삭제합니다.")
        delete_user(3)
        print(f"유저를 3명 삭제하였습니다. | 현재 유저 수: {_total_user_count}명")

    def do_del10(self, arg):
        """유저 10명 삭제"""
        if not self.initialize:
            print("프로그램이 초기화되지 않았습니다. init 명령어를 사용하세요.")
            return
        print("유저를 10명 삭제합니다.")
        delete_user(10)
        print(f"유저를 10명 삭제하였습니다. | 현재 유저 수: {_total_user_count}명")

    def do_exit(self, arg):
        """프로그램 종료"""
        print("테스트를 종료합니다.")
        return True


if __name__ == "__main__":
    APIShell().cmdloop()
