# 강의 썸네일 배경 이미지 자동 생성기

Supabase에서 강의 데이터를 불러와 AI 이미지 생성 API로 썸네일 배경 이미지를 자동으로 생성하는 Streamlit 웹 애플리케이션입니다.

## 주요 기능

- **Supabase 강의 데이터 연동**: Supabase DB에서 강의 목록을 읽기 전용으로 조회 (제목, 카테고리, 키워드, 개념, 툴 등)
- **YAML 기반 프롬프트 자동 생성**: 스타일 템플릿 + 카테고리 컨텍스트 + 기본 규칙을 조합하여 이미지 프롬프트 자동 구성
- **4가지 AI 모델 비교 생성**: Nano Banana 2 (Fast), Nano Banana Pro (Quality), Nano Banana (Efficient), Imagen 4.0
- **Streamlit 웹 UI**: 강의 선택, 스타일 선택, 모델 선택, 프롬프트 수정, 이미지 비교 및 선택
- **이미지 저장**: 선택한 이미지를 로컬 `output/` 폴더에 PNG 파일로 저장
- **생성 로그**: JSONL 형식으로 생성 이력 기록

## 기술 스택

- **Language**: Python 3.11+
- **Web UI**: Streamlit
- **AI API**: Google Gemini (Nano Banana 2, Pro, Efficient) / Google Imagen 4.0
- **Database**: Supabase (읽기 전용)
- **Image Processing**: Pillow
- **설정 관리**: PyYAML, python-dotenv

## 설치

```bash
git clone https://github.com/zzarru/thumbnail-bg-generator.git
cd thumbnail-bg-generator
pip install -r requirements.txt
```

## 환경 변수 설정

`.env.example`을 복사하여 `.env` 파일을 생성합니다:

```bash
cp .env.example .env
```

`.env` 파일에 아래 값을 설정합니다:

```
GOOGLE_API_KEY=your_google_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

| 변수명 | 설명 |
|---|---|
| `GOOGLE_API_KEY` | Google AI Studio에서 발급받은 API 키 |
| `SUPABASE_URL` | Supabase 프로젝트 URL |
| `SUPABASE_ANON_KEY` | Supabase 익명(anon) API 키 |

## 사용법

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속합니다.

**사용 흐름:**

1. 사이드바에서 강의를 검색하거나 목록에서 선택합니다.
2. 이미지 스타일을 선택합니다 (미니멀리스트, 사이버펑크, 수채화, 모던 테크, 추상).
3. 사용할 AI 모델을 하나 이상 선택하고 모델당 생성 장수를 설정합니다.
4. 자동 생성된 프롬프트를 확인하고 필요시 수정합니다.
5. **이미지 생성** 버튼을 클릭합니다.
6. 생성된 이미지 중 원하는 이미지의 **선택** 버튼을 클릭하면 `output/` 폴더에 저장됩니다.

## 프로젝트 구조

```
thumbnail-bg-generator/
├── app.py                      # Streamlit 메인 애플리케이션
├── requirements.txt            # 의존성 패키지 목록
├── .env.example                # 환경 변수 예시 파일
├── config/
│   ├── __init__.py
│   ├── settings.py             # 환경 변수 및 경로 설정
│   └── models.yaml             # AI 모델 목록 및 설정
├── core/
│   ├── __init__.py
│   ├── db_reader.py            # Supabase 강의 데이터 조회
│   ├── prompt_builder.py       # YAML 템플릿 기반 프롬프트 생성
│   ├── image_generator.py      # Gemini / Imagen API 이미지 생성
│   └── logger.py               # 생성 이력 JSONL 로깅
├── templates/
│   ├── styles.yaml             # 이미지 스타일 템플릿
│   ├── category_context.yaml   # 강의 카테고리별 시각 컨텍스트
│   └── base_prompt.yaml        # 공통 기본 프롬프트 규칙
├── tests/
│   ├── __init__.py
│   ├── test_db_reader.py       # DBReader 단위 테스트
│   ├── test_prompt_builder.py  # PromptBuilder 단위 테스트
│   ├── test_image_generator.py # ImageGenerator 단위 테스트
│   └── test_logger.py          # GenerationLogger 단위 테스트
├── output/                     # 생성된 이미지 저장 폴더 (자동 생성)
│   ├── temp/                   # 임시 이미지 저장
│   └── logs/                   # 생성 로그 (generation_log.jsonl)
├── docs/                       # 설계 문서
└── mockup/                     # UI 목업
```

## AI 모델 목록

| 모델 키 | 모델명 | 제공사 | 특징 |
|---|---|---|---|
| `nano_banana_2` | Nano Banana 2 (Fast) | Gemini | 빠른 생성 |
| `nano_banana_pro` | Nano Banana Pro (Quality) | Gemini | 고품질 |
| `nano_banana` | Nano Banana (Efficient) | Gemini | 효율적 |
| `imagen` | Imagen 4.0 | Imagen | Google Imagen API |

## 라이선스

MIT License
