import os
import sys
import json
import time
import shutil
import psutil
import tkinter as tk
from tkinter import messagebox

# ================= PATHS =================

def get_asset_path(path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

APPDATA = os.getenv("APPDATA")
DATA_DIR = os.path.join(APPDATA, "temp_watcher")
DATA_FILE = os.path.join(DATA_DIR, "folders.json")

os.makedirs(DATA_DIR, exist_ok=True)

CHECK_INTERVAL = 3

# ================= DATA =================

def load_folders():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_folders(folders):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(folders, f, indent=4)

# ================= EXPLORER =================

def explorer_open_on(path):
    path = path.lower()
    for proc in psutil.process_iter(["name", "cmdline"]):
        if proc.info["name"] == "explorer.exe":
            cmd = proc.info.get("cmdline")
            if not cmd:
                continue
            for arg in cmd:
                if path in arg.lower():
                    return True
    return False

# ================= UI =================

def ask_delete(path):
    root = tk.Tk()
    root.withdraw()

    res = messagebox.askyesno(
        "Suppression",
        f"Supprimer ce dossier ?\n\n{path}\n\n(et tout son contenu)"
    )

    root.destroy()
    return res

# ================= MAIN =================

def main():
    asked = set()

    while True:
        folders = load_folders()
        updated = False

        for folder in folders[:]:
            if not os.path.exists(folder):
                folders.remove(folder)
                asked.discard(folder)
                updated = True
                continue

            if not explorer_open_on(folder):
                if folder not in asked:
                    if ask_delete(folder):
                        try:
                            shutil.rmtree(folder)
                        except Exception:
                            pass
                        folders.remove(folder)
                        asked.discard(folder)
                        updated = True
                    else:
                        asked.add(folder)

        if updated:
            save_folders(folders)

        time.sleep(CHECK_INTERVAL)

# ================= START =================

if __name__ == "__main__":
    main()
