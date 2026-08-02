import sys
import asyncio

class StreamRenderer:
    def __init__(self):
        self.is_active = False

    def start(self):
        self.is_active = True
        print("Assistant >\n\n", end="", flush=True)

    async def render_chunk(self, chunk: str):
        if self.is_active and chunk:
            for char in chunk:
                if not self.is_active:
                    break
                print(char, end="", flush=True)
                await asyncio.sleep(0.01)

    def finish(self):
        self.is_active = False
        print("\n", flush=True)
