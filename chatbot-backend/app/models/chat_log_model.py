from sqlalchemy import Column, Integer, String, Text, Float, Boolean, TIMESTAMP, text
from app.database import Base


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    user_name = Column(String(100), nullable=True)
    user_role = Column(String(20), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    similarity_score = Column(Float, nullable=True)
    is_fallback = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))