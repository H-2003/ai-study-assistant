def chunk_text(text, max_chars=10000):
    if len(text) <= max_chars:
        return text
    return text[:max_chars]