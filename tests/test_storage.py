from alarm_clock.models import Alarm
from alarm_clock.storage import AlarmStorage


def test_save_and_load(tmp_path):
    path = tmp_path / "alarms.json"
    storage = AlarmStorage(path)
    alarms = [Alarm(1, "07:30", "Wake up"), Alarm(2, "09:00", "Meeting", False)]
    storage.save(alarms)
    loaded = storage.load()
    assert loaded == alarms
