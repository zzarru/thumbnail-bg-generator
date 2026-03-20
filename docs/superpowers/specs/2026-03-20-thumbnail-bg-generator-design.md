# PRD: 강의 썸네일 배경 이미지 자동 생성기

## 1. 배경 및 문제 정의

### 문제
- 400여 개 이상의 강의 썸네일 배경 이미지를 대량 생산해야 함
- 팀 내 디자이너가 부재한 상황
- 썸네일 배경 이미지만으로 강의를 시각적으로 구별해야 함 (텍스트, 강사 이미지 없음)

### 목표
- AI 이미지 생성 API를 활용하여 강의 데이터 기반으로 썸네일 배경 이미지를 자동 생성
- 프롬프트 템플릿 시스템으로 다양한 스타일을 시도하고 최적의 결과물을 찾을 수 있도록 지원

## 2. 사용자 및 사용 시나리오

### 사용자
- **1단계**: 본인이 직접 사용하며 프롬프트 품질 테스트 및 개선
- **2단계**: 안정화 후 팀 내 자동화 웹에 핵심 로직 통합

### 핵심 시나리오
1. 사용자가 웹 UI에서 강의를 검색/선택한다
2. 스타일 템플릿과 모델을 선택하고 생성 장수를 지정한다
3. 조합된 프롬프트를 미리보기하고 필요시 수정한다
4. 이미지 생성 버튼을 누르면 선택한 모델별로 이미지가 생성된다
5. 생성된 이미지들을 비교하고 최종 1장을 선택하여 저장한다

## 3. 기술 스택

| 구분 | 기술 |
|------|------|
| Language | Python |
| Web UI | Streamlit |
| AI 이미지 생성 | Google Gemini API (Nano Banana 2, Pro, 기본), Imagen 4.0, OpenAI (GPT Image, DALL-E 3) |
| DB | Supabase (PostgreSQL) - 읽기 전용 |
| Image Processing | Pillow |

## 4. 데이터 소스

### Supabase 강의 테이블 (읽기 전용)

이미지 생성에 활용할 필드:

| 필드 | 타입 | 활용 방식 |
|------|------|----------|
| category | varchar | 카테고리별 색상 톤/팔레트 구분 |
| level | varchar | 이미지 복잡도/톤 결정 |
| title | text | 주제 파악 → 이미지 소재 결정 |
| keywords | _text | 구체적인 시각 요소 힌트 |
| concept | varchar | 전체적인 분위기/컨셉 방향 |
| tools | _text | 관련 기술 소재 참고 |

나머지 필드(subtitle, description, goals 등)는 이미지 생성에 사용하지 않음.

> **참고**: Supabase 테이블명은 구현 시 확인 필요. 카테고리는 현재 "인공지능", "웹 프로그래밍" 2개이며, 추가 시 카테고리 컨텍스트 매핑도 함께 추가.

## 5. AI 모델 구성

| 모델 | ID | 특징 | Provider |
|------|-----|------|----------|
| Nano Banana 2 | gemini-3.1-flash-image-preview | 속도 최적화 | Gemini |
| Nano Banana Pro | gemini-3-pro-image-preview | 고품질 전문 자산 | Gemini |
| Nano Banana | gemini-2.5-flash-image | 효율성 중심 | Gemini |
| Imagen 4.0 | imagen-4.0-generate-001 | Google Imagen | Imagen |
| GPT Image | gpt-image-1 | OpenAI 최신 이미지 생성 | OpenAI |
| DALL-E 3 | dall-e-3 | OpenAI 범용 이미지 생성 | OpenAI |

- 사용자가 1개 이상 모델을 복수 선택 가능
- 모델당 사용자가 지정한 장수만큼 생성
- 모델 설정은 YAML 파일로 관리 (코드 수정 없이 추가/변경 가능)

## 6. 프롬프트 템플릿 시스템

### 구조
```
최종 프롬프트 = 스타일 템플릿
             + 카테고리 컨텍스트
             + 키워드/concept 시각 요소
             + 공통 규칙
```

### 스타일 템플릿 (YAML)
```yaml
minimalist:
  name: "미니멀리스트"
  prompt: "minimalist flat design, clean composition, soft gradient background"

cyberpunk:
  name: "사이버펑크"
  prompt: "cyberpunk style, neon lights, dark background, futuristic elements"

watercolor:
  name: "수채화"
  prompt: "watercolor painting style, soft edges, artistic brush strokes"
```

- YAML 파일로 관리하여 비개발자도 추가/편집 가능
- 공통 규칙: `"no text, no human faces, background image only"`

### 카테고리별 컨텍스트
카테고리-컨텍스트 매핑도 YAML로 관리:

```yaml
# templates/category_context.yaml
인공지능:
  visual_elements: "AI, neural network, data visualization, algorithm, deep learning"
  color_tone: "blue-purple gradient"
웹 프로그래밍:
  visual_elements: "code editor, browser window, web interface, responsive design"
  color_tone: "green-blue gradient"
```

새 카테고리 추가 시 이 파일에 항목만 추가하면 됨.

## 7. 이미지 생성 사양

| 항목 | 값 |
|------|-----|
| 비율 | 3:2 (630x410에 가장 근사) |
| 출력 형식 | PNG |
| 저장 위치 | 로컬 `output/` 폴더 |
| 최종 파일명 | `{lecture_id}_thumbnail.png` |
| 후보 이미지 저장 | `output/temp/{lecture_id}_{model}_{n}.png` (생성 세션 중 임시 저장, 최종 선택 시 정식 파일명으로 이동) |
| 생성 장수 제한 | 모델당 최대 5장, 1회 요청 시 총 최대 20장 (비용/속도 보호) |

## 8. UI 구성 (Streamlit)

### 사이드바
- 강의 검색/선택 (Supabase DB 조회)
- 스타일 템플릿 선택
- 모델 복수 선택
- 생성 장수 입력
- 생성 버튼

### 메인 영역
- 조합된 최종 프롬프트 미리보기 (직접 수정 가능)
- 생성된 이미지 격자 비교 (모델명, 번호 표시)
- 이미지별 [선택] 버튼으로 최종 저장

## 9. 프로젝트 구조

```
thumbnail-bg-generator/
├── app.py                    # Streamlit 진입점
├── config/
│   ├── models.yaml           # 모델 설정
│   └── settings.py           # 환경변수, DB 접속 등
├── templates/
│   ├── styles.yaml           # 스타일 템플릿
│   ├── category_context.yaml # 카테고리별 시각 요소/색상 매핑
│   └── base_prompt.yaml      # 공통 프롬프트 규칙 ("no text, no faces" 등)
├── core/
│   ├── db_reader.py          # Supabase 읽기 전용 조회
│   ├── prompt_builder.py     # 프롬프트 조합 로직
│   └── image_generator.py    # 모델별 API 호출 (Gemini/Imagen)
├── output/                   # 최종 선택된 이미지 저장
│   ├── temp/                 # 후보 이미지 임시 저장
│   └── logs/                 # 생성 이력 로그 (generation_log.jsonl)
├── .env                      # API 키, DB 접속 정보
├── .env.example
├── requirements.txt
└── README.md
```

### 모듈 역할
- **core/db_reader.py**: Supabase에서 강의 목록/상세 조회 (읽기 전용)
- **core/prompt_builder.py**: 스타일 템플릿 + 강의 데이터 → 최종 프롬프트 조합
- **core/image_generator.py**: 모델별 API 호출. Gemini 3종은 genai SDK, Imagen은 Imagen API로 분기
- **app.py**: Streamlit UI

## 10. 개발 단계

### Phase 1: 단일 생성 (MVP)
- 단일 강의 선택 → 프롬프트 조합 → 이미지 생성 → 비교 → 선택 저장
- 프롬프트 템플릿 시스템 구축
- 프롬프트 품질 개선 및 스타일 확보
- 에러 핸들링: API 실패 시 해당 모델 결과만 에러 표시, 성공한 모델 결과는 정상 노출
- 생성 이력 로깅: `output/logs/generation_log.jsonl`에 프롬프트, 모델, 선택 여부 기록

### Phase 2: 일괄 생성
- 조건별 필터링/전체 강의 일괄 생성
- 진행률 표시, 에러 핸들링

### Phase 3: 팀 웹 통합
- 핵심 로직(core/)을 기존 팀 자동화 웹에 이식
- Supabase Storage 업로드 + DB 경로 업데이트

## 11. 환경 변수

```
GOOGLE_API_KEY=            # Google Gemini/Imagen API 키
OPENAI_API_KEY=            # OpenAI GPT Image/DALL-E API 키
SUPABASE_URL=              # Supabase 프로젝트 URL
SUPABASE_ANON_KEY=         # Supabase 익명 키 (읽기 전용)
```
