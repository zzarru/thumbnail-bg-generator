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
