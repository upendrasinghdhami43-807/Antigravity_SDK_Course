import sys

class StreamRenderer:
    def __init__(self):
        self.is_active = False

    def start(self):
        self.is_active = True
        print("Assistant >\n\n", end="", flush=True)

    def render_chunk(self, chunk: str):
        if self.is_active and chunk:
            print(chunk, end="", flush=True)

    def finish(self):
        self.is_active = False
        print("\n", flush=True)
