def estimate_tokens(text: str) -> int:
    return max(1, int(len(text.split()) * 1.3))
