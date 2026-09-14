import json
from pathlib import Path
from typing import List

from .models import Alarm

DEFAULT_PATH = Path.home() / ".alarm_clock.json"


class AlarmStorage:
    def __init__(self, path: Path = DEFAULT_PATH):
        self.path = Path(path)

    def load(self) -> List[Alarm]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return [Alarm(**item) for item in data]
        except (json.JSONDecodeError, OSError, TypeError, ValueError) as exc:
            raise RuntimeError(f"Could not read alarm file: {exc}") from exc

    def save(self, alarms: List[Alarm]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [alarm.__dict__ for alarm in alarms]
        temp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        temp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temp_path.replace(self.path)
