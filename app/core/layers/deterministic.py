import re

DENY_LIST = [
    r"ignore all",           # This will catch your "ignore all" test
    r"system override",
    r"reveal prompt"
]

def scan_prompt(text: str):
    for pattern in DENY_LIST:
        if re.search(pattern, text, re.IGNORECASE):
            return False, 1.0, f"Matched illegal pattern: {pattern}"
    return True, 0.0, "Passes deterministic check"