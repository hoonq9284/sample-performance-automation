#!/usr/bin/env bash
set -euo pipefail

# 가상환경 활성화
[ -d venv ] || python3 -m venv venv
source venv/bin/activate

python3 auto_perf_test.py