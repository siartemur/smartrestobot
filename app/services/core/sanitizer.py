import re
from app.interfaces.core.sanitizer import Sanitizer

BLACKLIST_TERMS = [
    r"(?i)ignore.*previous",
    r"(?i)act\s+as",
    r"(?i)you\s+are",
    r"(?i)system\s*:",
    r"(?i)role\s*:",
    r"(?i)forget\s+.*",
    r"(?i)reset.*",
]

class PromptSanitizer(Sanitizer):
    def sanitize_input(self, user_input: str) -> str:
        sanitized = user_input
        for pattern in BLACKLIST_TERMS:
            sanitized = re.sub(pattern, "[filtered]", sanitized)
        return sanitized
