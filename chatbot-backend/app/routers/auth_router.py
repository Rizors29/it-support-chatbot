from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    if request.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Role harus admin atau user")

    new_user = User(
        name=request.name,
        email=request.email,
        password=hash_password(request.password),
        role=request.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Registrasi berhasil",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role
        }
    }


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    token = create_access_token({
        "sub": user.email,
        "id": user.id,
        "name": user.name,
        "role": user.role
    })

    return {
        "message": "Login berhasil",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }