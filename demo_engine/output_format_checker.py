import json

class OutputFormatChecker:
    """
    Validates that demo_output.jsonl matches DEMO_OUTPUT_FORMAT.md.
    """

    REQUIRED_FIELDS = ["ts_ms", "event", "session_id"]

    def __init__(self, path: str):
        self.path = path
        self.errors = []

    def validate_line(self, line: str, index: int):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            self.errors.append(f"Line {index}: invalid JSON")
            return

        for field in self.REQUIRED_FIELDS:
            if field not in obj:
                self.errors.append(f"Line {index}: missing field '{field}'")

        if not isinstance(obj.get("ts_ms", None), int):
            self.errors.append(f"Line {index}: ts_ms must be int")

        if not isinstance(obj.get("event", None), str):
            self.errors.append(f"Line {index}: event must be string")

        if not isinstance(obj.get("session_id", None), str):
            self.errors.append(f"Line {index}: session_id must be string")

    def validate(self):
        with open(self.path, "r") as f:
            for idx, line in enumerate(f, start=1):
                self.validate_line(line, idx)

        return self.errors