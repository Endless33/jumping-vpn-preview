class Emitter:
    def __init__(self, path: str):
        self.f = open(path, "w")

    def emit(self, event):
        self.f.write(event.to_jsonl() + "\n")

    def close(self):
        self.f.close()