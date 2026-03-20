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
