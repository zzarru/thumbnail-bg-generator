from dataclasses import dataclass
from pathlib import Path

import base64

import yaml
from google import genai
from google.genai import types
from openai import OpenAI


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
        openai_api_key: str = "",
    ):
        self.api_key = api_key
        self.openai_api_key = openai_api_key
        self.max_per_model = max_per_model
        self.max_total = max_total
        self._models = self._load_models(Path(models_config_path))
        self._client = genai.Client(api_key=api_key) if api_key else None
        self._openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None

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
                    elif provider == "openai":
                        self._generate_openai(prompt, model_config["model_id"], filepath)

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
                image_config=types.ImageConfig(aspect_ratio="16:9"),
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
                aspect_ratio="16:9",
                number_of_images=1,
            ),
        )
        if response.generated_images:
            image = response.generated_images[0].image
            image.save(str(output_path))
            return
        raise RuntimeError("No image in Imagen response")

    def _generate_openai(self, prompt: str, model_id: str, output_path: Path):
        if model_id == "gpt-image-1":
            response = self._openai_client.images.generate(
                model=model_id,
                prompt=prompt,
                n=1,
                size="1536x1024",
            )
        else:
            # DALL-E 3: 지원 크기 1024x1024, 1024x1792, 1792x1024
            response = self._openai_client.images.generate(
                model=model_id,
                prompt=prompt,
                n=1,
                size="1792x1024",
                response_format="b64_json",
            )

        image_data_item = response.data[0]
        if image_data_item.b64_json:
            image_bytes = base64.b64decode(image_data_item.b64_json)
            with open(output_path, "wb") as f:
                f.write(image_bytes)
        elif image_data_item.url:
            import urllib.request
            urllib.request.urlretrieve(image_data_item.url, str(output_path))
