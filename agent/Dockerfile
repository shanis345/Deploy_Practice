# 베이스 이미지는 빌드 인자로 고정한다. (Day 3에서 최신 패치 태그로 올려 재빌드)
ARG BASE=python:3.12.7-slim
ARG APP_VERSION=0.1.0

# ---- 빌드 스테이지: 의존성만 설치 ----
FROM ${BASE} AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/build/deps -r requirements.txt

# ---- 실행 스테이지 ----
FROM ${BASE}
ARG APP_VERSION
# non-root 사용자 (보안 심의 필수 항목). OpenShift는 임의 UID를 주므로 GID 0 쓰기 권한도 준다.
RUN useradd --create-home --uid 10001 --gid 0 appuser \
 && mkdir -p /app/config /app/tmp \
 && chgrp -R 0 /app && chmod -R g=u /app
WORKDIR /app
COPY --from=builder /build/deps /app/deps
COPY app.py .
ENV PYTHONPATH=/app/deps \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/app \
    APP_VERSION=${APP_VERSION}
USER 10001
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/healthz')"
CMD ["python", "app.py"]
