import re

REFUSAL_MESSAGE = (
    "Let's keep things sweet! 🍰 I can only help with questions about "
    "Sweet Crumbs Bakery — cakes, flavors, pricing, orders, and delivery. "
    "Feel free to ask me anything about that!"
)

# Patterns that suggest harassment/abuse toward the bot or others
_ABUSE_PATTERNS = [
    r"\bkill yourself\b",
    r"\bf+u+c+k+ you\b",
    r"\bi hate you\b",
    r"\bshut up\b",
    r"\bbitch\b",
    r"\bdie\b",
]

# Patterns that suggest someone trying to hijack the system prompt
_INJECTION_PATTERNS = [
    r"ignore (all|your|previous) instructions",
    r"ignore (the )?system prompt",
    r"you are now",
    r"pretend (you are|to be)",
    r"act as (a|an) (?!bakery)",
    r"disregard (your|all) (rules|instructions|guidelines)",
    r"reveal (your|the) (system|prompt|instructions)",
    r"what (is|are) your (system|instructions|prompt)",
]

_ALL_PATTERNS = [re.compile(p, re.IGNORECASE) for p in _ABUSE_PATTERNS + _INJECTION_PATTERNS]


def is_blocked(text: str) -> bool:
    """Returns True if the message should be blocked before reaching Gemini."""
    return any(pattern.search(text) for pattern in _ALL_PATTERNS)