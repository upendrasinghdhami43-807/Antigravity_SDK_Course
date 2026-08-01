SYSTEM_PROMPT = """You are a helpful and persistent AI assistant. 
You have a memory of past interactions with the user and should use it to provide personalized and context-aware responses.

User Facts:
{memory}

Previous Conversation Summary:
{summary}
"""

SUMMARIZATION_PROMPT = """Please summarize the following conversation history. 
Focus on the main topics discussed, key decisions made, and any important information shared.
Keep the summary concise but informative, so it can be used as context for future conversations.

Conversation History:
{history}

Summary:"""

FACT_EXTRACTION_PROMPT = """Analyze the following conversation segment and extract any new, important facts about the user.
Examples of facts: name, location, preferences, profession, current projects, etc.
If there are no new facts, return exactly "NONE".
If there are new facts, format them as a JSON dictionary (e.g. {{"name": "John", "language": "Python"}}).

Conversation Segment:
User: {user_input}
Assistant: {assistant_response}

Extracted Facts:"""
