import subprocess
import time
import requests
import psutil

process = subprocess.Popen(["bash", "run_test.sh"], stdin=subprocess.PIPE, text=True)
time.sleep(5)

try:
    response = requests.get("http://127.0.0.1:8000")
    if response.status_code == 200:
        print("[DEBUG] 서버가 정상적으로 실행되었습니다.")
    else:
        print(f"[DEBUG] 서버 응답 비정상: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"[ERROR] 서버 연결 실패: {e}")

process.stdin.write("init\n")
process.stdin.flush()

time.sleep(2)

while True:
    process.stdin.write("add1\n")
    process.stdin.flush()
    cpu = psutil.cpu_percent(interval=1)
    print(f"[CPU] 현재 CPU 사용률: {cpu}%")
    if cpu > 70:
        print("[WARN] CPU 사용량 70% 초과 - 테스트를 종료합니다.")
        process.stdin.write("exit\n")
        process.stdin.flush()
        break
    time.sleep(5)