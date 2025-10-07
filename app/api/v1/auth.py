from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import create_access_token, verify_password
from app.db.models import User
from app.schemas.auth import LoginInput, Token

router = APIRouter()


@router.post("/login", response_model=Token)
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash) or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(sub=user.email, extra={"role": user.role})
    return {"status_code": status.HTTP_200_OK, "access_token": token, "token_type": "bearer"}
