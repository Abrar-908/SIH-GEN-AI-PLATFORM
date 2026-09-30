import json
from pathlib import Path
from app.core.config import EXPORTS_DIR

class TextExporter:
    @staticmethod
    def export_text(filename: str, content: str) -> str:
        filepath = EXPORTS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return str(filepath)

    @staticmethod
    def export_json(filename: str, data: dict) -> str:
        filepath = EXPORTS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return str(filepath)
