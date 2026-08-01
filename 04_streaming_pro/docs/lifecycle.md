# Stream Lifecycle

Every streamed response goes through a specific lifecycle governed by the `StreamManager`.

1. **Idle**: The system is waiting for user input.
2. **Connecting**: The user has submitted a prompt. The network request is dispatched. The "First-Token Latency" timer starts.
3. **Streaming**: The first chunk arrives. The latency timer stops. The renderer starts rapidly flushing chunks to the screen, and the buffer collects them.
4. **Interrupted (Optional)**: If the user presses `Ctrl+C`, the `StreamManager` catches the cancellation. It forcefully closes the network connection and stops the renderer. The buffer retains whatever was generated up to that point.
5. **Completed**: The network connection closes naturally.
6. **Saving**: The buffer is collapsed into a single string. The text is passed to the tokenizer, the memory extractor, and the history manager. The system returns to Idle.
