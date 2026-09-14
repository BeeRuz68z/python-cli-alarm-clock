import pytest
from datetime import datetime
from alarm_clock.models import Alarm


def test_alarm_matches_same_minute():
    alarm = Alarm(1, "07:30", "Wake up")
    assert alarm.matches(datetime(2026, 9, 14, 7, 30))


def test_disabled_alarm_does_not_match():
    alarm = Alarm(1, "07:30", enabled=False)
    assert not alarm.matches(datetime(2026, 9, 14, 7, 30))


def test_invalid_time_is_rejected():
    with pytest.raises(ValueError):
        Alarm(1, "25:99")
