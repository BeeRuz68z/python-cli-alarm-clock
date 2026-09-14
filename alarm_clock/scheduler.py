import time as time_module
from datetime import datetime
from typing import Callable, List

from .models import Alarm


class Scheduler:
    def __init__(self, alarms: List[Alarm], on_alarm: Callable[[Alarm], None]):
        self.alarms = alarms
        self.on_alarm = on_alarm

    def run(self, sleep_seconds: float = 1.0) -> None:
        last_triggered = set()
        print("Alarm clock running... Press Ctrl+C to stop.")
        while True:
            now = datetime.now()
            minute_key = now.strftime("%Y-%m-%d %H:%M")
            for alarm in self.alarms:
                key = (alarm.id, minute_key)
                if alarm.matches(now) and key not in last_triggered:
                    last_triggered.add(key)
                    self.on_alarm(alarm)
            last_triggered = {key for key in last_triggered if key[1] == minute_key}
            time_module.sleep(sleep_seconds)
