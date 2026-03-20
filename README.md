# Thumbnail BG Generator

AI를 활용한 강의 썸네일 배경 이미지 자동 생성기

## 개요

강의 주제와 키워드를 입력하면 AI 이미지 생성 API를 통해 썸네일 배경 이미지를 자동으로 생성하는 프로그램입니다.

## 주요 기능

- 강의 주제/키워드 기반 배경 이미지 자동 생성
- Google Imagen API 지원
- 다양한 이미지 크기 및 스타일 옵션
- 배치 생성 지원 (여러 이미지 한번에 생성)

## 기술 스택

- **Language**: Python
- **AI API**: Google Imagen / Nanobanana
- **Image Processing**: Pillow

## 설치

```bash
git clone https://github.com/zzarru/thumbnail-bg-generator.git
cd thumbnail-bg-generator
pip install -r requirements.txt
```

## 환경 변수 설정

```bash
cp .env.example .env
```

`.env` 파일에 API 키를 설정합니다:

```
GOOGLE_API_KEY=your_api_key_here
```

## 사용법

```bash
python main.py --topic "Python 기초" --style "modern" --size "1280x720"
```

## 프로젝트 구조

```
thumbnail-bg-generator/
├── main.py              # 메인 실행 파일
├── config.py            # 설정 관리
├── generators/          # 이미지 생성 모듈
│   ├── imagen.py        # Google Imagen API
│   └── nanobanana.py    # Nanobanana API
├── utils/               # 유틸리티
├── output/              # 생성된 이미지 저장
├── requirements.txt
├── .env.example
└── README.md
```

## 라이선스

MIT License
