# from datetime import datetime
# from typing import List, Optional
# from pydantic import BaseModel


# class ChatMessage(BaseModel):
#     role: str  # "user" or "assistant"
#     content: str
#     timestamp: datetime


# class ChatSession(BaseModel):
#     user_id: int
#     session_id: str
#     messages: List[ChatMessage]
#     started_at: datetime
#     last_interaction: datetime

#     def add_message(self, role: str, content: str):
#         now = datetime.utcnow()
#         self.messages.append(ChatMessage(role=role, content=content, timestamp=now))
#         self.last_interaction = now
