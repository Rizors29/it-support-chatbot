from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, text
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum("admin", "user"), nullable=False, default="user")
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))