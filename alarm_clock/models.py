from dataclasses import dataclass
from datetime import datetime, time


@dataclass
class Alarm:
    id: int
    alarm_time: str
    label: str = "Alarm"
    enabled: bool = True

    def __post_init__(self):
        datetime.strptime(self.alarm_time, "%H:%M")
        self.alarm_time = self.alarm_time

    def matches(self, current: datetime) -> bool:
        return self.enabled and current.strftime("%H:%M") == self.alarm_time
