class Tokenizer:
    """
    Interface for estimating tokens. 
    Phase 2 uses character-based estimation. Real tokenizers (tiktoken, Gemini API) can be swapped here.
    """
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Roughly estimate tokens (e.g. 1 token ~= 4 chars)."""
        if not text:
            return 0
        return max(1, len(text) // 4)
