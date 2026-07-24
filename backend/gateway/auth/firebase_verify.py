import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.shared.config import settings
from backend.shared.logging_config import logger

security = HTTPBearer()

def initialize_firebase():
    if not firebase_admin._apps:
        try:
            if settings.FIREBASE_PROJECT_ID and settings.FIREBASE_CLIENT_EMAIL and settings.FIREBASE_PRIVATE_KEY:
                cred = credentials.Certificate({
                    "type": "service_account",
                    "project_id": settings.FIREBASE_PROJECT_ID,
                    "client_email": settings.FIREBASE_CLIENT_EMAIL,
                    "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
                })
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDK initialized with service account credentials.")
            else:
                logger.warning("Firebase credentials incomplete. Running Firebase auth in mock fallback mode.")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin SDK: {e}")

initialize_firebase()

async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    token = credentials.credentials
    try:
        if firebase_admin._apps:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        else:
            # Fallback mock decoded token for dev mode
            return {
                "uid": f"mock_user_{token[:10]}",
                "email": "demo@forgeai.dev",
                "phone_number": "+15550192834"
            }
    except Exception as e:
        logger.error(f"Firebase token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
