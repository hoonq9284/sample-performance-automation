#!/usr/bin/env bash
set -euo pipefail

# 가상환경 활성화
[ -d venv ] || python3 -m venv venv
source venv/bin/activate

# sample-performance-automation 서버 백그라운드 실행
uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1 &
SERVER_PID=$!
trap 'kill ${SERVER_PID} 2>/dev/null || true' EXIT

# 서버 기동 대기 (최대 5초)
echo "[INFO] 서버 기동 중..."
for i in {1..25}; do
  if curl -sSf http://127.0.0.1:8000/ >/dev/null 2>&1; then
    echo "[INFO] 서버 기동 완료!"
    break
  fi
  sleep 0.2
done

# 테스트 실행 (인자 없으면 인터랙티브, 있으면 순차 실행)
if [ "$#" -eq 0 ]; then
  python3 -u test_suite.py
else
  printf "%s\n" "$@" | python3 -u test_suite.py
fi