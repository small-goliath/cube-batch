# 프로젝트 설정 가이드

## 1. 가상환경 적용
Python 가상환경을 설정하고 활성화

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. 의존성 패키지 설치
프로젝트에서 필요한 패키지를 `requirements.txt`를 이용하여 설치

```bash
pip install -r requirements.txt
```

## 3. 크론탭 초기화
Crontab을 설정하기 위해 아래 명령어를 실행

```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

## 4. 환경 변수 설정 (`.env` 파일 필요 내용)
프로젝트 실행을 위해 `.env` 파일을 생성하고 아래 내용을 포함해야 함

```
referer=<보안계정 정보 URI>  # [보안관리] > 본인 이름 클릭 후 확인
password=<계속 사용할 패스워드>
icon=<dialog 알림에 사용할 아이콘>
log=<로그파일 경로>
home=<로그인 uri>
```
