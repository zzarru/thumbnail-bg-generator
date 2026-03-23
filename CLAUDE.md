# CLAUDE.md

## Commit Convention (Gitmoji)

커밋 메시지 작성 시 반드시 [Gitmoji](https://gitmoji.dev/) 컨벤션을 따릅니다.

### Format

```
<gitmoji> <subject> (50자 이내)

<body> (선택, 왜 변경했는지)
```

### Gitmoji Reference (from gitmoji.dev)

| Emoji | Code | Description |
|-------|------|-------------|
| 🎨 | `:art:` | 코드 구조/포맷 개선 |
| ⚡️ | `:zap:` | 성능 개선 |
| 🔥 | `:fire:` | 코드/파일 삭제 |
| 🐛 | `:bug:` | 버그 수정 |
| 🚑️ | `:ambulance:` | 긴급 핫픽스 |
| ✨ | `:sparkles:` | 새 기능 추가 |
| 📝 | `:memo:` | 문서 추가/수정 |
| 🚀 | `:rocket:` | 배포 |
| 💄 | `:lipstick:` | UI/스타일 변경 |
| 🎉 | `:tada:` | 프로젝트 시작 |
| ✅ | `:white_check_mark:` | 테스트 추가/수정/통과 |
| 🔒️ | `:lock:` | 보안/프라이버시 이슈 수정 |
| 🔐 | `:closed_lock_with_key:` | 시크릿 추가/수정 |
| 🔖 | `:bookmark:` | 릴리스/버전 태그 |
| 🚨 | `:rotating_light:` | 컴파일러/린터 경고 수정 |
| 🚧 | `:construction:` | 작업 중 (WIP) |
| 💚 | `:green_heart:` | CI 빌드 수정 |
| ⬇️ | `:arrow_down:` | 의존성 다운그레이드 |
| ⬆️ | `:arrow_up:` | 의존성 업그레이드 |
| 📌 | `:pushpin:` | 의존성 버전 고정 |
| 👷 | `:construction_worker:` | CI 빌드 시스템 추가/수정 |
| 📈 | `:chart_with_upwards_trend:` | 분석/트래킹 코드 추가/수정 |
| ♻️ | `:recycle:` | 코드 리팩토링 |
| ➕ | `:heavy_plus_sign:` | 의존성 추가 |
| ➖ | `:heavy_minus_sign:` | 의존성 제거 |
| 🔧 | `:wrench:` | 설정 파일 추가/수정 |
| 🔨 | `:hammer:` | 개발 스크립트 추가/수정 |
| 🌐 | `:globe_with_meridians:` | 국제화/번역 |
| ✏️ | `:pencil2:` | 오타 수정 |
| 💩 | `:poop:` | 개선 필요한 코드 작성 |
| ⏪️ | `:rewind:` | 변경사항 되돌리기 |
| 🔀 | `:twisted_rightwards_arrows:` | 브랜치 머지 |
| 📦️ | `:package:` | 컴파일 파일/패키지 추가/수정 |
| 👽️ | `:alien:` | 외부 API 변경에 따른 코드 수정 |
| 🚚 | `:truck:` | 리소스 이동/이름 변경 |
| 📄 | `:page_facing_up:` | 라이선스 추가/수정 |
| 💥 | `:boom:` | Breaking changes 도입 |
| 🍱 | `:bento:` | 에셋 추가/수정 |
| ♿️ | `:wheelchair:` | 접근성 개선 |
| 💡 | `:bulb:` | 소스코드 주석 추가/수정 |
| 🍻 | `:beers:` | 음주 코딩 |
| 💬 | `:speech_balloon:` | 텍스트/리터럴 추가/수정 |
| 🗃️ | `:card_file_box:` | DB 관련 변경 |
| 🔊 | `:loud_sound:` | 로그 추가/수정 |
| 🔇 | `:mute:` | 로그 제거 |
| 👥 | `:busts_in_silhouette:` | 기여자 추가/수정 |
| 🚸 | `:children_crossing:` | UX/사용성 개선 |
| 🏗️ | `:building_construction:` | 아키텍처 변경 |
| 📱 | `:iphone:` | 반응형 디자인 |
| 🤡 | `:clown_face:` | Mock 관련 작업 |
| 🥚 | `:egg:` | 이스터에그 추가/수정 |
| 🙈 | `:see_no_evil:` | .gitignore 추가/수정 |
| 📸 | `:camera_flash:` | 스냅샷 추가/수정 |
| ⚗️ | `:alembic:` | 실험적 작업 |
| 🔍️ | `:mag:` | SEO 개선 |
| 🏷️ | `:label:` | 타입 추가/수정 |
| 🌱 | `:seedling:` | 시드 파일 추가/수정 |
| 🚩 | `:triangular_flag_on_post:` | 피처 플래그 추가/수정/제거 |
| 🥅 | `:goal_net:` | 에러 캐치 |
| 💫 | `:dizzy:` | 애니메이션/트랜지션 추가/수정 |
| 🗑️ | `:wastebasket:` | 정리 필요한 코드 deprecate |
| 🛂 | `:passport_control:` | 인가/권한/역할 관련 작업 |
| 🩹 | `:adhesive_bandage:` | 비핵심 이슈 간단 수정 |
| 🧐 | `:monocle_face:` | 데이터 탐색/검사 |
| ⚰️ | `:coffin:` | 죽은 코드 제거 |
| 🧪 | `:test_tube:` | 실패하는 테스트 추가 |
| 👔 | `:necktie:` | 비즈니스 로직 추가/수정 |
| 🩺 | `:stethoscope:` | 헬스체크 추가/수정 |
| 🧱 | `:bricks:` | 인프라 관련 변경 |
| 🧑‍💻 | `:technologist:` | 개발자 경험(DX) 개선 |
| 💸 | `:money_with_wings:` | 스폰서십/결제 인프라 추가 |
| 🧵 | `:thread:` | 멀티스레딩/동시성 코드 추가/수정 |
| 🦺 | `:safety_vest:` | 유효성 검증 코드 추가/수정 |

### Rules

1. **하나의 커밋 = 하나의 의도** (Gitmoji가 2개 필요하면 커밋을 분리)
2. subject는 한국어 또는 영어 (프로젝트 기존 스타일 따름)
3. Gitmoji는 텍스트 코드(`:sparkles:`)가 아닌 **실제 이모지(✨)** 사용
4. body에는 "왜" 변경했는지 작성 (선택)

### Examples

```
✨ OpenAI 이미지 생성 프로바이더 추가

gpt-image-1과 dall-e-3 모델을 지원하여
무료 Gemini 할당량 소진 시 대안 제공
```

```
🐛 packt_products 테이블 PK를 product_id로 수정
```

```
📝 비개발자를 위한 바이브 코딩 튜토리얼 추가
```

```
♻️ 이미지 생성기에서 모델별 파라미터 분리
```

```
🔧 .env.example에 OPENAI_API_KEY 항목 추가
```
