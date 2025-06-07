from enum import Enum

class PromptVersion(str, Enum):
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"

class AgentType(str, Enum):
    GENERAL = "general"
    MENU = "menu"
    RESERVATION = "reservation"
