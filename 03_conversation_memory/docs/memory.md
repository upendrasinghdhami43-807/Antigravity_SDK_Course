# Memory Strategy

We divide memory into two distinct layers to optimize token usage and context relevance.

## Short-Term Memory
Stored in `history.json`. It contains the exact back-and-forth transcript of the recent conversation. Because of LLM token limits (Context Window), we can only feed a limited number of these raw messages into the model at any one time.

## Long-Term Memory
Stored in `memory.json`. When the Assistant replies, we run a secondary background prompt to extract core facts (e.g., User's Name: John, Favorite Language: Python). These facts are injected into the System Prompt. This allows the Assistant to remember things from 10,000 messages ago without needing the actual transcript of that conversation.
