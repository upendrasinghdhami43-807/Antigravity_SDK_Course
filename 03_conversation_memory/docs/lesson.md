# Module 3: Conversation Memory

In this module, we transitioned from a simple, stateless chat application into a persistent AI assistant capable of long-term interaction.

## Key Concepts Learned

1. **Short-Term Memory (Context Window)**: What the LLM can hold in a single API request.
2. **Long-Term Memory (Fact Storage)**: Extracting and persisting facts independently from the raw chat history.
3. **Session Management**: Distinguishing between different periods of interaction.
4. **Token Management**: Dealing with LLM token limits by truncating or summarizing history.

By separating these concerns into `history.py`, `memory.py`, and `context.py`, we created a robust architecture ready for RAG and Vector Databases in future modules.
