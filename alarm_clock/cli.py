import argparse
from datetime import datetime

from .models import Alarm
from .scheduler import Scheduler
from .storage import AlarmStorage


def parse_time(value: str) -> str:
    try:
        datetime.strptime(value, "%H:%M")
    except ValueError as exc:
        raise argparse.ArgumentTypeError("time must use HH:MM in 24-hour format") from exc
    return value


def next_id(alarms):
    return max((a.id for a in alarms), default=0) + 1


def build_parser():
    parser = argparse.ArgumentParser(prog="alarm-clock", description="A simple Python CLI alarm clock")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Create an alarm")
    add.add_argument("time", type=parse_time, help="Alarm time, HH:MM")
    add.add_argument("--label", default="Alarm")

    sub.add_parser("list", help="List alarms")

    delete = sub.add_parser("delete", help="Delete an alarm")
    delete.add_argument("id", type=int)

    enable = sub.add_parser("enable", help="Enable an alarm")
    enable.add_argument("id", type=int)

    disable = sub.add_parser("disable", help="Disable an alarm")
    disable.add_argument("id", type=int)

    sub.add_parser("run", help="Start the alarm scheduler")
    return parser


def find_alarm(alarms, alarm_id):
    return next((a for a in alarms if a.id == alarm_id), None)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = AlarmStorage()

    try:
        alarms = storage.load()
        if args.command == "add":
            alarm = Alarm(next_id(alarms), args.time, args.label)
            alarms.append(alarm)
            storage.save(alarms)
            print(f"Created alarm #{alarm.id}: {alarm.alarm_time} - {alarm.label}")

        elif args.command == "list":
            if not alarms:
                print("No alarms configured.")
                return
            print(f"{'ID':<4} {'TIME':<7} {'STATUS':<9} LABEL")
            for alarm in sorted(alarms, key=lambda a: a.alarm_time):
                status = "enabled" if alarm.enabled else "disabled"
                print(f"{alarm.id:<4} {alarm.alarm_time:<7} {status:<9} {alarm.label}")

        elif args.command in {"enable", "disable"}:
            alarm = find_alarm(alarms, args.id)
            if alarm is None:
                parser.error(f"alarm #{args.id} does not exist")
            alarm.enabled = args.command == "enable"
            storage.save(alarms)
            print(f"Alarm #{alarm.id} {'enabled' if alarm.enabled else 'disabled'}.")

        elif args.command == "delete":
            alarm = find_alarm(alarms, args.id)
            if alarm is None:
                parser.error(f"alarm #{args.id} does not exist")
            alarms.remove(alarm)
            storage.save(alarms)
            print(f"Deleted alarm #{args.id}.")

        elif args.command == "run":
            def notify(alarm):
                print(f"\\a[{alarm.alarm_time}] ALARM: {alarm.label}")

            Scheduler(alarms, notify).run()

    except RuntimeError as exc:
        parser.error(str(exc))
    except KeyboardInterrupt:
        print("\\nAlarm clock stopped.")
