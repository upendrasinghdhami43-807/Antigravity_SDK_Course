import json
import os

HISTORY_FILE = "data/history.json"

class History:
    def __init__(self):
        self.messages = []
        os.makedirs("data", exist_ok=True)
        self.load()

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        self.save()

    def save(self):
        try:
            with open(HISTORY_FILE, "w") as f:
                json.dump(self.messages, f, indent=4)
        except Exception:
            pass

    def load(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    self.messages = json.load(f)
            except Exception:
                self.messages = []

    def clear(self):
        self.messages = []
        self.save()
