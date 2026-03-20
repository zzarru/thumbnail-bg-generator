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
