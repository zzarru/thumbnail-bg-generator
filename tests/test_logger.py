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

        entry2 = json.loads(lines[1])
        assert entry2["selected"] is True
