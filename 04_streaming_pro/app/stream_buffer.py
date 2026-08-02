class StreamBuffer:
    def __init__(self):
        self.buffer = []
        
    def add_chunk(self, chunk: str):
        self.buffer.append(chunk)
        
    def get_full_text(self) -> str:
        return "".join(self.buffer)
        
    def clear(self):
        self.buffer.clear()
