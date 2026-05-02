import re

# Patterns for common sensitive data
PII_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
    "API_KEY": r"(sk-[a-zA-Z0-9]{20,})|(AIza[0-9A-Za-z-_]{35})",
    "PHONE": r"\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b",
    "IPV4": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
}

def sanitize_response(text: str) -> str:
    sanitized_text = text
    for label, pattern in PII_PATTERNS.items():
        # Replace the sensitive match with a redaction label
        sanitized_text = re.sub(pattern, f"[{label}_REDACTED]", sanitized_text)
    
    return sanitized_text