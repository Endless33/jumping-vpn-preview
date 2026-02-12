import json
import os
import time


def now_ms():
    return int(time.time() * 1000)


class JsonlLogger:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # каждый запуск очищает лог
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("")

    def emit(self, event_type: str, **data):
        event = {
            "ts_ms": now_ms(),
            "type": event_type,
            **data
        }

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")