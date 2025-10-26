# sample-performance-automation
FastAPI 를 이용한 성능 부하 테스트 자동화 스터디

## 필요 패키지
- python 3.13.0

## 실행 방법
1. git clone {repository_url}
2. cd {repository_url}
3. pip install -r requirements.txt
4. chmod +x ./run_test.sh
5. chmod +x ./auto_test.sh
5. (수동 테스트의 경우) `./run_test.sh`
6. (자동 테스트의 경우) `./auto_test.sh`

## 프로세스 가이드
### 수동 테스트
- 직접 InteractiveShell 을 이용하여, CLI 를 이용해 부하 테스트 가능

### 자동 테스트
- 일정 시간마다 유저를 1명씩 추가하고, CPU 사용량을 점진적으로 체크함
- CPU 사용량이 사전에 정의된 임계치에 도달했을 때, 테스트 강제 종료 및 최대 유저 확인 가능