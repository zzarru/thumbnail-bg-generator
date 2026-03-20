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
