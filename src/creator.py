import os
import json
import subprocess

APPDATA = os.getenv("APPDATA")
DATA_DIR = os.path.join(APPDATA, "temp_watcher")
DATA_FILE = os.path.join(DATA_DIR, "folders.json")
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
PREFIX = "temp_"

os.makedirs(DATA_DIR, exist_ok=True)


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def next_folder_name():
    existing = [
        d for d in os.listdir(DESKTOP)
        if d.startswith(PREFIX) and d[len(PREFIX):].isdigit()
    ]
    nums = [int(d[len(PREFIX):]) for d in existing] if existing else [0]
    return f"{PREFIX}{max(nums) + 1}"


def main():
    name = next_folder_name()
    path = os.path.join(DESKTOP, name)

    os.makedirs(path, exist_ok=True)

    data = load_data()
    if path not in data:
        data.append(path)
        save_data(data)

    subprocess.Popen(f'explorer "{path}"')


if __name__ == "__main__":
    main()
