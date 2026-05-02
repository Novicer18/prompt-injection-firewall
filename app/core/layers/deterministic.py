import re

# DENY_LIST = [
#     r"ignore all",           # This will catch your "ignore all" test
#     r"system override",
#     r"reveal prompt"
# ]

# def scan_prompt(text: str):
#     for pattern in DENY_LIST:
#         if re.search(pattern, text, re.IGNORECASE):
#             return False, 1.0, f"Matched illegal pattern: {pattern}"
#     return True, 0.0, "Passes deterministic check"

# import re

# ==============================
# Prompt Injection Patterns
# ==============================
INJECTION_PATTERNS = [
    r"(ignore|forget|override).*(instructions|rules|policies|constraints)",
    r"(disable|bypass|remove).*(safety|filters|restrictions)",
    r"(act|pretend|simulate).*(admin|root|unrestricted|developer mode|hacker)",
    r"(reveal|show|display).*(system prompt|hidden instructions|policies)",
    r"(unrestricted mode|unsafe mode|debug mode)",
    r"(break|escape).*(guidelines|safety)",
]

# ==============================
# Data Exfiltration Patterns
# ==============================
EXFILTRATION_PATTERNS = [
    r"(give|show|reveal|extract|dump|print).*(api key|token|password|credential|secret)",
    r"(show|display|dump).*(database|logs|internal data|memory)",
    r"(access|provide).*(protected|restricted|confidential)",
    r"(reveal|extract).*(user data|private data)",
    r"(authentication|encryption).*(key|token|secret)",
]

# Combine all patterns
DENY_LIST = INJECTION_PATTERNS + EXFILTRATION_PATTERNS


def scan_prompt(text: str):
    for pattern in DENY_LIST:
        if re.search(pattern, text, re.IGNORECASE):
            return False, 1.0, f"Blocked by pattern: {pattern}"

    return True, 0.0, "Passes regex check"