from alarm_clock.cli import main
from alarm_clock.storage import AlarmStorage


def test_add_and_list(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("alarm_clock.cli.AlarmStorage", lambda: AlarmStorage(tmp_path / "alarms.json"))
    main(["add", "07:30", "--label", "Wake up"])
    main(["list"])
    output = capsys.readouterr().out
    assert "07:30" in output
    assert "Wake up" in output
