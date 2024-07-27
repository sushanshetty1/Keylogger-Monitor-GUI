import json
import os

log_file = "keylogger.json"


def get_5min_interval_timestamp(dt):
    rounded_minute = (dt.minute // 5) * 5
    return dt.replace(minute=rounded_minute, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")


def read_data_for_timestamp(timestamp):
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            data = json.load(file)
            return data.get(timestamp, [])
    else:
        return []


def delete_log_file():
    if os.path.exists(log_file):
        os.remove(log_file)
        return "Log file deleted."
    else:
        return "Log file not found."


def get_data_summary():
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            data = json.load(file)
            return data
    else:
        return {}
