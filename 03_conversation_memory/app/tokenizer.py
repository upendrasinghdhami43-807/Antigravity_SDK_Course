def estimate_tokens(text: str) -> int:
    """
    Provides a rough estimate of tokens in a string.
    In a real-world scenario, you might use a specific tokenizer library (like tiktoken for OpenAI)
    or the model's built-in count_tokens API (for Gemini).
    As a general heuristic, 1 token is roughly 4 characters in English.
    """
    if not text:
        return 0
    return len(text) // 4
