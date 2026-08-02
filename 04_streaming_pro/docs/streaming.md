# Understanding Streaming

Streaming involves managing a continuous flow of data rather than a single bulk download. 

## Chunk Processing
When Gemini streams a response, it doesn't send individual characters or entire sentences. It sends "chunks". A chunk usually contains a few words or sub-word tokens. 

Your job as a developer is to handle these chunks efficiently.

1. **Rendering**: The moment a chunk arrives, it should be immediately printed to the screen so the user sees it instantly. We use `print(chunk, end="", flush=True)` to force the terminal to draw it without waiting for a newline.
2. **Buffering**: While rendering the chunks, you must also save them. We append each chunk to an internal list (the "buffer"). 
3. **Completion**: When the stream closes, we join the buffer (`"".join(buffer)`) to get the final complete string. This final string is what gets saved to history and memory.

## Async Iterators
In Python, streaming is usually handled via an **Asynchronous Iterator**. Instead of a standard `for` loop, you use an `async for` loop:

```python
async for chunk in response:
    print(chunk.text)
```
This tells Python to pause execution of this function while waiting for the next chunk to arrive over the network, freeing up the CPU to handle other tasks (like UI updates or catching keyboard interrupts).
