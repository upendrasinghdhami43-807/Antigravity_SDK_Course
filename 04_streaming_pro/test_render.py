import asyncio
from app.stream_renderer import StreamRenderer

async def main():
    renderer = StreamRenderer()
    renderer.start()
    await renderer.render_chunk("hello, this is a streaming test.")
    renderer.finish()

if __name__ == "__main__":
    asyncio.run(main())
