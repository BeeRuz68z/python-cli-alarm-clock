# Alarm Clock — Python CLI

A small, dependency-light command-line alarm clock built as a Senior Software Engineer take-home exercise.

## Requirements

- Python 3.10+
- No web UI
- No database
- Standard library for the application
- `pytest` only for tests

## Features

- Add alarms using 24-hour `HH:MM` format
- List alarms
- Enable/disable alarms
- Delete alarms
- Run a foreground scheduler
- Persist configuration to `~/.alarm_clock.json`
- Terminal bell notification
- Graceful Ctrl+C shutdown
- Unit tests for model, storage, and CLI behavior

## Quick start

```bash
python -m alarm_clock add 07:30 --label "Wake up"
python -m alarm_clock list
python -m alarm_clock disable 1
python -m alarm_clock enable 1
python -m alarm_clock delete 1
python -m alarm_clock run
```

Run tests:

```bash
python -m pip install pytest
pytest -q
```

## Design decisions

### Why JSON?
The exercise prohibits a database but does not require alarms to be ephemeral. JSON provides simple persistence without adding infrastructure or dependencies. Writes go through a temporary file before replacement to reduce the chance of leaving a partially written file.

### Why separate modules?
`models.py` owns alarm behavior, `storage.py` owns persistence, `scheduler.py` owns time polling, and `cli.py` translates user input into application operations. This keeps the core logic testable and avoids putting all behavior into argument handlers.

### Scheduler trade-off
The scheduler polls once per second. For a 30-minute exercise this is easier to reason about than a more complex event scheduler. The alarm is keyed by date + minute so it fires at most once during its matching minute.

### Scope intentionally excluded
Recurring alarms, custom audio files, GUI features, background OS services, and multi-user support were excluded to keep the core experience reliable and reviewable within the time limit.

## Edge cases considered

- Invalid time formats
- Disabled alarms
- Missing alarm IDs
- Empty alarm list
- Corrupt/unreadable persistence file
- Duplicate firing within the same minute
- Graceful Ctrl+C shutdown

## AI-assisted development

AI was used as an engineering assistant for requirements refinement, architecture alternatives, implementation scaffolding, and edge-case review. Generated suggestions were reviewed and validated with tests before being retained. The final design intentionally favors simplicity, explicit boundaries, and testability over feature count.
