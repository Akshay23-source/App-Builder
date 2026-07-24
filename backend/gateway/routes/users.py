from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.db.session import get_async_db
from backend.db.models import User
from backend.shared.schemas import UserResponse, TokenResponse
from backend.gateway.auth.firebase_verify import verify_firebase_token
from backend.gateway.auth.jwt_handler import create_access_token
from backend.shared.logging_config import logger

router = APIRouter(prefix="/users", tags=["Users & Auth"])

@router.post("/verify-firebase", response_model=TokenResponse)
async def auth_with_firebase(
    decoded_token: dict = Depends(verify_firebase_token),
    db: AsyncSession = Depends(get_async_db)
):
    uid = decoded_token.get("uid")
    email = decoded_token.get("email")
    phone_number = decoded_token.get("phone_number")

    if not uid:
        raise HTTPException(status_code=400, detail="Firebase token missing uid")

    # Find or create user
    result = await db.execute(select(User).where(User.firebase_uid == uid))
    user = result.scalars().first()

    if not user:
        user = User(
            firebase_uid=uid,
            email=email,
            phone_number=phone_number
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    jwt_token = create_access_token({"sub": user.id, "firebase_uid": uid})
    return TokenResponse(
        access_token=jwt_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    decoded_token: dict = Depends(verify_firebase_token),
    db: AsyncSession = Depends(get_async_db)
):
    uid = decoded_token.get("uid")
    result = await db.execute(select(User).where(User.firebase_uid == uid))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")
    return UserResponse.model_validate(user)
