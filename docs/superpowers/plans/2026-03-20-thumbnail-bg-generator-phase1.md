# Thumbnail BG Generator Phase 1 (MVP) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 단일 강의를 선택하여 AI 이미지 생성 API로 썸네일 배경 이미지를 생성하고, 여러 모델/스타일 결과를 비교하여 최종 선택 저장하는 MVP를 구축한다.

**Architecture:** Streamlit 웹 UI → Core Engine (DB 조회, 프롬프트 조합, 이미지 생성) → 로컬 파일 저장. Core 모듈은 독립적으로 동작하며, Streamlit은 이를 조합하는 UI 레이어.

**Tech Stack:** Python 3.11+, Streamlit, google-genai SDK, supabase-py, Pillow, PyYAML, python-dotenv

**Spec:** `docs/superpowers/specs/2026-03-20-thumbnail-bg-generator-design.md`

---

## File Structure

| File | Responsibility |
|------|----------------|
| `config/models.yaml` | AI 모델 ID, 이름, provider 정의 |
| `config/settings.py` | 환경변수 로드, 경로 상수 |
| `templates/styles.yaml` | 스타일 프롬프트 템플릿 |
| `templates/category_context.yaml` | 카테고리별 시각 요소/색상 매핑 |
| `templates/base_prompt.yaml` | 공통 프롬프트 규칙 |
| `core/__init__.py` | 패키지 초기화 |
| `core/db_reader.py` | Supabase 읽기 전용 조회 |
| `core/prompt_builder.py` | 템플릿 + DB 데이터 → 최종 프롬프트 조합 |
| `core/image_generator.py` | 모델별 API 호출 (Gemini/Imagen) |
| `core/logger.py` | 생성 이력 JSONL 로깅 |
| `app.py` | Streamlit UI 진입점 |
| `tests/test_prompt_builder.py` | prompt_builder 단위 테스트 |
| `tests/test_image_generator.py` | image_generator 단위 테스트 |
| `tests/test_db_reader.py` | db_reader 단위 테스트 |
| `requirements.txt` | Python 의존성 |
| `.env.example` | 환경변수 템플릿 |
| `.gitignore` | output/, .env 등 제외 |

---

## Task 1: 프로젝트 초기 설정

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `config/__init__.py`
- Create: `core/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: requirements.txt 생성**

```txt
streamlit>=1.45.0
google-genai>=1.14.0
supabase>=2.15.0
Pillow>=11.0.0
PyYAML>=6.0.2
python-dotenv>=1.1.0
pytest>=8.3.0
```

- [ ] **Step 2: .env.example 생성**

```
GOOGLE_API_KEY=your_google_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

- [ ] **Step 3: .gitignore 생성**

```
.env
output/
__pycache__/
*.pyc
.venv/
```

- [ ] **Step 4: 패키지 __init__.py 파일 생성**

빈 파일: `config/__init__.py`, `core/__init__.py`, `tests/__init__.py`

- [ ] **Step 5: output 디렉토리 구조 생성**

```bash
mkdir -p output/temp output/logs
```

- [ ] **Step 6: 의존성 설치**

```bash
pip install -r requirements.txt
```

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .env.example .gitignore config/__init__.py core/__init__.py tests/__init__.py
git commit -m "chore: initialize project structure and dependencies"
```

---

## Task 2: 설정 및 YAML 템플릿 파일

**Files:**
- Create: `config/settings.py`
- Create: `config/models.yaml`
- Create: `templates/styles.yaml`
- Create: `templates/category_context.yaml`
- Create: `templates/base_prompt.yaml`

- [ ] **Step 1: config/settings.py 생성**

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = OUTPUT_DIR / "temp"
LOG_DIR = OUTPUT_DIR / "logs"
TEMPLATES_DIR = BASE_DIR / "templates"
CONFIG_DIR = BASE_DIR / "config"

MAX_IMAGES_PER_MODEL = 5
MAX_IMAGES_TOTAL = 20
IMAGE_ASPECT_RATIO = "3:2"
IMAGE_FORMAT = "png"
```

- [ ] **Step 2: config/models.yaml 생성**

```yaml
nano_banana_2:
  name: "Nano Banana 2 (Fast)"
  model_id: "gemini-3.1-flash-image-preview"
  provider: "gemini"

nano_banana_pro:
  name: "Nano Banana Pro (Quality)"
  model_id: "gemini-3-pro-image-preview"
  provider: "gemini"

nano_banana:
  name: "Nano Banana (Efficient)"
  model_id: "gemini-2.5-flash-image"
  provider: "gemini"

imagen:
  name: "Imagen 4.0"
  model_id: "imagen-4.0-generate-001"
  provider: "imagen"
```

- [ ] **Step 3: templates/styles.yaml 생성**

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

modern_tech:
  name: "모던 테크"
  prompt: "modern technology aesthetic, sleek surfaces, geometric shapes, digital atmosphere"

abstract:
  name: "추상"
  prompt: "abstract art style, bold colors, flowing shapes, artistic composition"
```

- [ ] **Step 4: templates/category_context.yaml 생성**

```yaml
인공지능:
  visual_elements: "AI, neural network, data visualization, algorithm, deep learning"
  color_tone: "blue-purple gradient"

웹 프로그래밍:
  visual_elements: "code editor, browser window, web interface, responsive design"
  color_tone: "green-blue gradient"
```

- [ ] **Step 5: templates/base_prompt.yaml 생성**

```yaml
rules:
  - "no text or letters anywhere in the image"
  - "no human faces or people"
  - "background image only, suitable for thumbnail overlay"
  - "high quality, visually appealing"
  - "3:2 aspect ratio composition"
```

- [ ] **Step 6: Commit**

```bash
git add config/settings.py config/models.yaml templates/
git commit -m "feat: add configuration and prompt template files"
```

---

## Task 3: Supabase DB Reader

**Files:**
- Create: `core/db_reader.py`
- Create: `tests/test_db_reader.py`

- [ ] **Step 1: 테스트 작성**

```python
# tests/test_db_reader.py
import pytest
from unittest.mock import patch, MagicMock


def _make_mock_response(data):
    mock = MagicMock()
    mock.data = data
    return mock


class TestDBReader:
    @patch("core.db_reader.create_client")
    def test_get_lectures_returns_list(self, mock_create):
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.table.return_value.select.return_value.execute.return_value = (
            _make_mock_response([
                {"id": 1, "title": "Python 기초", "category": "웹 프로그래밍"},
                {"id": 2, "title": "딥러닝 입문", "category": "인공지능"},
            ])
        )

        from core.db_reader import DBReader
        reader = DBReader("http://fake-url", "fake-key")
        lectures = reader.get_lectures()

        assert len(lectures) == 2
        assert lectures[0]["title"] == "Python 기초"

    @patch("core.db_reader.create_client")
    def test_get_lecture_by_id(self, mock_create):
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = (
            _make_mock_response({
                "id": 1,
                "title": "Python 기초",
                "category": "웹 프로그래밍",
                "level": "입문",
                "keywords": ["python", "기초"],
                "concept": "프로그래밍 첫걸음",
                "tools": ["python", "vscode"],
            })
        )

        from core.db_reader import DBReader
        reader = DBReader("http://fake-url", "fake-key")
        lecture = reader.get_lecture_by_id(1)

        assert lecture["title"] == "Python 기초"
        assert lecture["category"] == "웹 프로그래밍"

    @patch("core.db_reader.create_client")
    def test_search_lectures(self, mock_create):
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        mock_client.table.return_value.select.return_value.ilike.return_value.execute.return_value = (
            _make_mock_response([
                {"id": 1, "title": "Python 기초", "category": "웹 프로그래밍"},
            ])
        )

        from core.db_reader import DBReader
        reader = DBReader("http://fake-url", "fake-key")
        results = reader.search_lectures("Python")

        assert len(results) == 1
        assert results[0]["title"] == "Python 기초"
```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

```bash
pytest tests/test_db_reader.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'core.db_reader'`

- [ ] **Step 3: core/db_reader.py 구현**

```python
from supabase import create_client, Client

LECTURE_FIELDS = "id, title, category, level, keywords, concept, tools"


class DBReader:
    def __init__(self, url: str, key: str, table_name: str = "lectures"):
        self.client: Client = create_client(url, key)
        self.table_name = table_name

    def get_lectures(self) -> list[dict]:
        response = (
            self.client.table(self.table_name)
            .select(LECTURE_FIELDS)
            .execute()
        )
        return response.data

    def get_lecture_by_id(self, lecture_id: int) -> dict:
        response = (
            self.client.table(self.table_name)
            .select(LECTURE_FIELDS)
            .eq("id", lecture_id)
            .single()
            .execute()
        )
        return response.data

    def search_lectures(self, query: str) -> list[dict]:
        response = (
            self.client.table(self.table_name)
            .select(LECTURE_FIELDS)
            .ilike("title", f"%{query}%")
            .execute()
        )
        return response.data
```

- [ ] **Step 4: 테스트 실행 — 통과 확인**

```bash
pytest tests/test_db_reader.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/db_reader.py tests/test_db_reader.py
git commit -m "feat: add Supabase DB reader with lecture query methods"
```

---

## Task 4: Prompt Builder

**Files:**
- Create: `core/prompt_builder.py`
- Create: `tests/test_prompt_builder.py`

- [ ] **Step 1: 테스트 작성**

```python
# tests/test_prompt_builder.py
import pytest
from core.prompt_builder import PromptBuilder


@pytest.fixture
def builder(tmp_path):
    styles_yaml = tmp_path / "styles.yaml"
    styles_yaml.write_text(
        'minimalist:\n  name: "미니멀리스트"\n  prompt: "minimalist flat design, clean composition"\n',
        encoding="utf-8",
    )

    category_yaml = tmp_path / "category_context.yaml"
    category_yaml.write_text(
        '인공지능:\n  visual_elements: "AI, neural network"\n  color_tone: "blue-purple gradient"\n',
        encoding="utf-8",
    )

    base_yaml = tmp_path / "base_prompt.yaml"
    base_yaml.write_text(
        'rules:\n  - "no text"\n  - "no human faces"\n  - "background image only"\n',
        encoding="utf-8",
    )

    return PromptBuilder(templates_dir=tmp_path)


class TestPromptBuilder:
    def test_get_styles_returns_dict(self, builder):
        styles = builder.get_styles()
        assert "minimalist" in styles
        assert styles["minimalist"]["name"] == "미니멀리스트"

    def test_build_prompt_combines_all_parts(self, builder):
        lecture = {
            "title": "딥러닝 입문",
            "category": "인공지능",
            "level": "입문",
            "keywords": ["딥러닝", "신경망"],
            "concept": "AI 기초 학습",
            "tools": ["pytorch"],
        }
        prompt = builder.build_prompt(lecture, style_key="minimalist")

        assert "minimalist flat design" in prompt
        assert "AI, neural network" in prompt
        assert "딥러닝" in prompt
        assert "no text" in prompt

    def test_build_prompt_unknown_category_skips_context(self, builder):
        lecture = {
            "title": "요리 강좌",
            "category": "요리",
            "level": "입문",
            "keywords": ["요리"],
            "concept": "기초 요리",
            "tools": [],
        }
        prompt = builder.build_prompt(lecture, style_key="minimalist")

        assert "minimalist flat design" in prompt
        assert "no text" in prompt

    def test_build_prompt_with_none_keywords(self, builder):
        lecture = {
            "title": "테스트",
            "category": "인공지능",
            "level": "입문",
            "keywords": None,
            "concept": None,
            "tools": None,
        }
        prompt = builder.build_prompt(lecture, style_key="minimalist")

        assert "minimalist flat design" in prompt
```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

```bash
pytest tests/test_prompt_builder.py -v
```

Expected: FAIL

- [ ] **Step 3: core/prompt_builder.py 구현**

```python
from pathlib import Path
import yaml


class PromptBuilder:
    def __init__(self, templates_dir: Path):
        self.templates_dir = Path(templates_dir)
        self._styles = self._load_yaml("styles.yaml")
        self._categories = self._load_yaml("category_context.yaml")
        self._base = self._load_yaml("base_prompt.yaml")

    def _load_yaml(self, filename: str) -> dict:
        filepath = self.templates_dir / filename
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_styles(self) -> dict:
        return self._styles

    def get_style_names(self) -> dict[str, str]:
        return {key: val["name"] for key, val in self._styles.items()}

    def build_prompt(self, lecture: dict, style_key: str) -> str:
        parts = []

        # 1. Style template
        style = self._styles.get(style_key, {})
        if style.get("prompt"):
            parts.append(style["prompt"])

        # 2. Category context
        category = lecture.get("category", "")
        cat_context = self._categories.get(category)
        if cat_context:
            parts.append(cat_context["visual_elements"])
            parts.append(f"{cat_context['color_tone']} color scheme")

        # 3. Lecture-specific elements
        keywords = lecture.get("keywords") or []
        if keywords:
            parts.append(", ".join(keywords))

        concept = lecture.get("concept")
        if concept:
            parts.append(f"theme: {concept}")

        tools = lecture.get("tools") or []
        if tools:
            parts.append(f"related to: {', '.join(tools)}")

        # 4. Level context
        level = lecture.get("level", "")
        if level:
            parts.append(f"{level} level complexity")

        # 5. Base rules
        rules = self._base.get("rules", [])
        parts.extend(rules)

        return ", ".join(parts)
```

- [ ] **Step 4: 테스트 실행 — 통과 확인**

```bash
pytest tests/test_prompt_builder.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/prompt_builder.py tests/test_prompt_builder.py
git commit -m "feat: add prompt builder with template composition"
```

---

## Task 5: Image Generator

**Files:**
- Create: `core/image_generator.py`
- Create: `tests/test_image_generator.py`

- [ ] **Step 1: 테스트 작성**

```python
# tests/test_image_generator.py
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from core.image_generator import ImageGenerator, GenerationResult


class TestImageGenerator:
    def test_load_models_from_yaml(self, tmp_path):
        models_yaml = tmp_path / "models.yaml"
        models_yaml.write_text(
            'test_model:\n  name: "Test"\n  model_id: "test-id"\n  provider: "gemini"\n',
            encoding="utf-8",
        )
        gen = ImageGenerator(api_key="fake", models_config_path=models_yaml)
        models = gen.get_available_models()

        assert "test_model" in models
        assert models["test_model"]["name"] == "Test"

    def test_validate_image_count_enforces_limits(self, tmp_path):
        models_yaml = tmp_path / "models.yaml"
        models_yaml.write_text(
            'a:\n  name: "A"\n  model_id: "a"\n  provider: "gemini"\n',
            encoding="utf-8",
        )
        gen = ImageGenerator(
            api_key="fake",
            models_config_path=models_yaml,
            max_per_model=5,
            max_total=20,
        )

        assert gen.validate_image_count(["a"], 5) is True
        assert gen.validate_image_count(["a"], 6) is False

    @patch("core.image_generator.genai")
    def test_generate_returns_results(self, mock_genai, tmp_path):
        models_yaml = tmp_path / "models.yaml"
        models_yaml.write_text(
            'nb2:\n  name: "NB2"\n  model_id: "gemini-3.1-flash-image-preview"\n  provider: "gemini"\n',
            encoding="utf-8",
        )

        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client

        mock_image = MagicMock()
        mock_image.save = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_part.as_image.return_value = mock_image

        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        gen = ImageGenerator(api_key="fake", models_config_path=models_yaml)
        results = gen.generate(
            prompt="test prompt",
            model_keys=["nb2"],
            count_per_model=1,
            output_dir=tmp_path,
            lecture_id="test123",
        )

        assert len(results) == 1
        assert results[0].model_key == "nb2"
        assert results[0].success is True

    def test_generate_handles_api_failure(self, tmp_path):
        models_yaml = tmp_path / "models.yaml"
        models_yaml.write_text(
            'nb2:\n  name: "NB2"\n  model_id: "gemini-3.1-flash-image-preview"\n  provider: "gemini"\n'
            'img:\n  name: "Imagen"\n  model_id: "imagen-4.0-generate-001"\n  provider: "imagen"\n',
            encoding="utf-8",
        )

        gen = ImageGenerator(api_key="fake", models_config_path=models_yaml)
        # Mock both providers to fail
        gen._generate_gemini = MagicMock(side_effect=RuntimeError("API error"))
        gen._generate_imagen = MagicMock(side_effect=RuntimeError("Imagen error"))

        results = gen.generate(
            prompt="test",
            model_keys=["nb2", "img"],
            count_per_model=1,
            output_dir=tmp_path,
            lecture_id="fail_test",
        )

        assert len(results) == 2
        assert all(r.success is False for r in results)
        assert "API error" in results[0].error
        assert "Imagen error" in results[1].error

    @patch("core.image_generator.genai")
    def test_generate_imagen_provider(self, mock_genai, tmp_path):
        models_yaml = tmp_path / "models.yaml"
        models_yaml.write_text(
            'img:\n  name: "Imagen"\n  model_id: "imagen-4.0-generate-001"\n  provider: "imagen"\n',
            encoding="utf-8",
        )

        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client

        mock_image = MagicMock()
        mock_image.save = MagicMock()

        mock_generated = MagicMock()
        mock_generated.image = mock_image

        mock_response = MagicMock()
        mock_response.generated_images = [mock_generated]
        mock_client.models.generate_images.return_value = mock_response

        gen = ImageGenerator(api_key="fake", models_config_path=models_yaml)
        results = gen.generate(
            prompt="test",
            model_keys=["img"],
            count_per_model=1,
            output_dir=tmp_path,
            lecture_id="img_test",
        )

        assert len(results) == 1
        assert results[0].success is True
        assert results[0].model_key == "img"
```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

```bash
pytest tests/test_image_generator.py -v
```

Expected: FAIL

- [ ] **Step 3: core/image_generator.py 구현**

```python
from dataclasses import dataclass
from pathlib import Path

import yaml
from google import genai
from google.genai import types


@dataclass
class GenerationResult:
    model_key: str
    model_name: str
    image_path: Path | None
    success: bool
    error: str | None = None


class ImageGenerator:
    def __init__(
        self,
        api_key: str,
        models_config_path: Path | str = "config/models.yaml",
        max_per_model: int = 5,
        max_total: int = 20,
    ):
        self.api_key = api_key
        self.max_per_model = max_per_model
        self.max_total = max_total
        self._models = self._load_models(Path(models_config_path))
        self._client = genai.Client(api_key=api_key)

    def _load_models(self, path: Path) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_available_models(self) -> dict:
        return self._models

    def validate_image_count(self, model_keys: list[str], count_per_model: int) -> bool:
        if count_per_model > self.max_per_model:
            return False
        if len(model_keys) * count_per_model > self.max_total:
            return False
        return True

    def generate(
        self,
        prompt: str,
        model_keys: list[str],
        count_per_model: int,
        output_dir: Path,
        lecture_id: str,
    ) -> list[GenerationResult]:
        results = []
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for model_key in model_keys:
            model_config = self._models[model_key]
            provider = model_config["provider"]

            for i in range(count_per_model):
                filename = f"{lecture_id}_{model_key}_{i + 1}.png"
                filepath = output_dir / filename

                try:
                    if provider == "gemini":
                        self._generate_gemini(prompt, model_config["model_id"], filepath)
                    elif provider == "imagen":
                        self._generate_imagen(prompt, model_config["model_id"], filepath)

                    results.append(GenerationResult(
                        model_key=model_key,
                        model_name=model_config["name"],
                        image_path=filepath,
                        success=True,
                    ))
                except Exception as e:
                    results.append(GenerationResult(
                        model_key=model_key,
                        model_name=model_config["name"],
                        image_path=None,
                        success=False,
                        error=str(e),
                    ))

        return results

    def _generate_gemini(self, prompt: str, model_id: str, output_path: Path):
        response = self._client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="3:2"),
            ),
        )
        for part in response.parts:
            if part.inline_data:
                image = part.as_image()
                image.save(str(output_path))
                return
        raise RuntimeError("No image in API response")

    def _generate_imagen(self, prompt: str, model_id: str, output_path: Path):
        response = self._client.models.generate_images(
            model=model_id,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                aspect_ratio="3:2",
                number_of_images=1,
            ),
        )
        if response.generated_images:
            image = response.generated_images[0].image
            image.save(str(output_path))
            return
        raise RuntimeError("No image in Imagen response")
```

- [ ] **Step 4: 테스트 실행 — 통과 확인**

```bash
pytest tests/test_image_generator.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/image_generator.py tests/test_image_generator.py
git commit -m "feat: add image generator with Gemini and Imagen support"
```

---

## Task 6: Generation Logger

**Files:**
- Create: `core/logger.py`
- Create: `tests/test_logger.py`

- [ ] **Step 1: 테스트 작성**

```python
# tests/test_logger.py
import json
import pytest
from core.logger import GenerationLogger


class TestGenerationLogger:
    def test_log_generation_creates_jsonl(self, tmp_path):
        log_file = tmp_path / "generation_log.jsonl"
        logger = GenerationLogger(log_file)

        logger.log(
            lecture_id="123",
            model_key="nb2",
            prompt="test prompt",
            image_path="/output/temp/123_nb2_1.png",
            selected=False,
        )

        lines = log_file.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 1

        entry = json.loads(lines[0])
        assert entry["lecture_id"] == "123"
        assert entry["model_key"] == "nb2"
        assert entry["selected"] is False
        assert "timestamp" in entry

    def test_log_multiple_entries(self, tmp_path):
        log_file = tmp_path / "generation_log.jsonl"
        logger = GenerationLogger(log_file)

        logger.log(lecture_id="1", model_key="a", prompt="p1", image_path="x", selected=False)
        logger.log(lecture_id="2", model_key="b", prompt="p2", image_path="y", selected=True)

        lines = log_file.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 2
```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

```bash
pytest tests/test_logger.py -v
```

Expected: FAIL

- [ ] **Step 3: core/logger.py 구현**

```python
import json
from datetime import datetime, timezone
from pathlib import Path


class GenerationLogger:
    def __init__(self, log_path: Path | str):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        lecture_id: str,
        model_key: str,
        prompt: str,
        image_path: str,
        selected: bool,
    ):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "lecture_id": lecture_id,
            "model_key": model_key,
            "prompt": prompt,
            "image_path": image_path,
            "selected": selected,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
```

- [ ] **Step 4: 테스트 실행 — 통과 확인**

```bash
pytest tests/test_logger.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/logger.py tests/test_logger.py
git commit -m "feat: add JSONL generation logger"
```

---

## Task 7: Streamlit UI

**Files:**
- Create: `app.py`

- [ ] **Step 1: app.py 구현**

```python
import shutil
import streamlit as st
from pathlib import Path

from config.settings import (
    GOOGLE_API_KEY,
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    TEMP_DIR,
    OUTPUT_DIR,
    LOG_DIR,
    TEMPLATES_DIR,
    CONFIG_DIR,
    MAX_IMAGES_PER_MODEL,
    MAX_IMAGES_TOTAL,
)
from core.db_reader import DBReader
from core.prompt_builder import PromptBuilder
from core.image_generator import ImageGenerator
from core.logger import GenerationLogger

st.set_page_config(page_title="썸네일 배경 생성기", layout="wide")
st.title("강의 썸네일 배경 이미지 생성기")


@st.cache_resource
def get_db_reader():
    return DBReader(SUPABASE_URL, SUPABASE_ANON_KEY)


@st.cache_resource
def get_prompt_builder():
    return PromptBuilder(TEMPLATES_DIR)


@st.cache_resource
def get_image_generator():
    return ImageGenerator(
        api_key=GOOGLE_API_KEY,
        models_config_path=CONFIG_DIR / "models.yaml",
    )


def get_logger():
    return GenerationLogger(LOG_DIR / "generation_log.jsonl")


# --- Sidebar ---
with st.sidebar:
    st.header("설정")

    # Lecture search & select
    db_reader = get_db_reader()
    search_query = st.text_input("강의 검색", placeholder="강의 제목 입력...")

    if search_query:
        lectures = db_reader.search_lectures(search_query)
    else:
        lectures = db_reader.get_lectures()

    if not lectures:
        st.warning("강의를 찾을 수 없습니다.")
        st.stop()

    lecture_options = {f"{lec['id']} - {lec['title']}": lec for lec in lectures}
    selected_label = st.selectbox("강의 선택", options=list(lecture_options.keys()))
    selected_lecture = lecture_options[selected_label]

    st.divider()

    # Style select
    prompt_builder = get_prompt_builder()
    style_names = prompt_builder.get_style_names()
    selected_style = st.selectbox(
        "스타일 선택",
        options=list(style_names.keys()),
        format_func=lambda x: style_names[x],
    )

    st.divider()

    # Model select
    generator = get_image_generator()
    available_models = generator.get_available_models()
    selected_models = st.multiselect(
        "모델 선택 (복수 가능)",
        options=list(available_models.keys()),
        default=[list(available_models.keys())[0]],
        format_func=lambda x: available_models[x]["name"],
    )

    # Image count
    count_per_model = st.number_input(
        "모델당 생성 장수",
        min_value=1,
        max_value=MAX_IMAGES_PER_MODEL,
        value=2,
    )

    total = len(selected_models) * count_per_model
    if total > MAX_IMAGES_TOTAL:
        st.error(f"총 {total}장 요청 — 최대 {MAX_IMAGES_TOTAL}장까지 가능합니다.")

    st.divider()
    generate_btn = st.button("이미지 생성", type="primary", disabled=(total > MAX_IMAGES_TOTAL))

# --- Main Area ---
# Prompt preview
prompt = prompt_builder.build_prompt(selected_lecture, selected_style)
edited_prompt = st.text_area("프롬프트 미리보기 (수정 가능)", value=prompt, height=150)

# Generation
if generate_btn:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    with st.spinner(f"{total}장 이미지 생성 중..."):
        results = generator.generate(
            prompt=edited_prompt,
            model_keys=selected_models,
            count_per_model=count_per_model,
            output_dir=TEMP_DIR,
            lecture_id=str(selected_lecture["id"]),
        )

    st.session_state["results"] = results

# Display results
if "results" in st.session_state:
    results = st.session_state["results"]
    st.subheader("생성 결과")

    cols_per_row = 3
    cols = st.columns(cols_per_row)

    for idx, result in enumerate(results):
        col = cols[idx % cols_per_row]
        with col:
            if result.success and result.image_path:
                st.image(str(result.image_path), caption=f"{result.model_name} #{idx + 1}")
                if st.button(f"선택", key=f"select_{idx}"):
                    # Save as final
                    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                    final_path = OUTPUT_DIR / f"{selected_lecture['id']}_thumbnail.png"
                    shutil.copy2(result.image_path, final_path)

                    # Log all results
                    logger = get_logger()
                    for r in results:
                        logger.log(
                            lecture_id=str(selected_lecture["id"]),
                            model_key=r.model_key,
                            prompt=edited_prompt,
                            image_path=str(r.image_path) if r.image_path else "",
                            selected=(r is result),
                        )

                    st.success(f"저장 완료: {final_path}")
            else:
                st.error(f"{result.model_name}: {result.error}")
```

- [ ] **Step 2: 로컬 실행 테스트**

```bash
streamlit run app.py
```

브라우저에서 확인:
- 사이드바에 강의 검색, 스타일/모델 선택, 장수 입력이 보이는지
- 프롬프트 미리보기 영역이 표시되는지
- (실제 API 키 설정 후) 이미지 생성 및 비교가 동작하는지

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: add Streamlit UI with full generation workflow"
```

---

## Task 8: README 업데이트 및 최종 정리

**Files:**
- Modify: `README.md`

- [ ] **Step 1: README.md 업데이트**

프로젝트의 실제 구조와 사용법에 맞게 README를 업데이트한다. 설치, 환경변수 설정, 실행 방법, 프로젝트 구조를 포함.

- [ ] **Step 2: 전체 테스트 실행**

```bash
pytest tests/ -v
```

Expected: 모든 테스트 PASS

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: update README with actual project setup and usage"
```
