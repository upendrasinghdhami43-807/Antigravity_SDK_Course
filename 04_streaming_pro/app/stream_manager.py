import asyncio
import time
from app.stream_buffer import StreamBuffer
from app.stream_renderer import StreamRenderer
from app.logger import get_logger

logger = get_logger("StreamManager")

class StreamManager:
    def __init__(self, agent, stats_mgr):
        self.agent = agent
        self.stats_mgr = stats_mgr
        self.buffer = StreamBuffer()
        self.renderer = StreamRenderer()
        self.is_streaming = False

    async def run_stream(self, prompt: str, use_streaming: bool = True) -> str:
        """
        Initiates the stream, chunks it out, renders it, and returns the final buffered string.
        Tracks first-token latency and chunk timing.
        """
        if not use_streaming:
            # Fallback to sync generation
            logger.info("Streaming disabled, using synchronous generation.")
            response, elapsed = self.agent.generate_response(prompt)
            print("Assistant >\n\n" + response + "\n")
            self.stats_mgr.add_response_time(elapsed)
            return response
            
        self.is_streaming = True
        self.buffer.clear()
        self.renderer.start()
        
        start_time = time.time()
        first_token_time = None
        
        try:
            # generate_stream returns an async generator
            async for chunk in self.agent.generate_stream(prompt):
                if not self.is_streaming:
                    logger.info("Stream was cancelled mid-flight.")
                    break
                    
                if chunk:
                    if first_token_time is None:
                        first_token_time = time.time() - start_time
                        self.stats_mgr.add_latency(first_token_time)
                        
                    self.renderer.render_chunk(chunk)
                    self.buffer.add_chunk(chunk)
                    
                # Yield control to the event loop occasionally
                await asyncio.sleep(0.001)
                
        except asyncio.CancelledError:
            logger.info("Stream cancelled via asyncio.")
        except Exception as e:
            logger.error(f"Stream error: {e}")
            self.renderer.render_chunk(f"\n[Error: {e}]")
        finally:
            self.renderer.finish()
            self.is_streaming = False
            
        total_elapsed = time.time() - start_time
        self.stats_mgr.add_response_time(total_elapsed)
        return self.buffer.get_full_text()
        
    def cancel_stream(self):
        self.is_streaming = False
