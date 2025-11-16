# Python 베이스 이미지 사용
FROM python:3.12-slim

# 작업 디렉토리 생성
WORKDIR /app

# 필요한 시스템 패키지 설치 (SQLite 사용 시 기본 포함)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Django 프로젝트 전체 복사
COPY . /app/

# static 파일 모아서 /staticfiles 로 저장
RUN python manage.py collectstatic --noinput

# Gunicorn 실행 (Django WSGI로 구동)
CMD ["gunicorn", "lotto_site.wsgi:application", "--bind", "0.0.0.0:8000"]