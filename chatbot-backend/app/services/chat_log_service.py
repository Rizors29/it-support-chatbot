import json
from sqlalchemy.orm import Session

from app.models.chat_log_model import ChatLog


def save_chat_log(
    db: Session,
    user: dict | None,
    question: str,
    result: dict,
):
    sources = result.get("sources", [])

    log = ChatLog(
        user_id=user.get("id") if user else None,
        user_name=user.get("name") if user else "Guest",
        user_role=user.get("role") if user else "guest",
        question=question,
        answer=result.get("answer", ""),
        sources=json.dumps(sources),
        category=result.get("category"),
        similarity_score=result.get("similarity_score"),
        is_fallback=result.get("is_fallback", False),
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log