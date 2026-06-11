from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token tidak valid"
        )


def require_admin(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Akses hanya untuk admin"
        )

    return user