import json
import os
import shutil

LOG_FILE = ".organizer_log.json"

def save_log(target_dir: str, operations: list[dict]) -> None:
    log_path = os.path.join(target_dir, LOG_FILE)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(operations, f, indent=2)

def rollback(target_dir: str) -> int:
    log_path = os.path.join(target_dir, LOG_FILE)
    if not os.path.exists(log_path):
        return 0
    with open(log_path, "r", encoding="utf-8") as f:
        operations = json.load(f)

    reverted = 0
    for op in reversed(operations):
        if os.path.exists(op["dest"]):
            shutil.move(op["dest"], op["src"])
            reverted += 1

    os.remove(log_path)
    return reverted
