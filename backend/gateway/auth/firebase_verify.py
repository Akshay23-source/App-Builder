import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.shared.config import settings
from backend.shared.logging_config import logger

security = HTTPBearer(auto_error=False)

def initialize_firebase():
    if not firebase_admin._apps:
        try:
            if (
                settings.FIREBASE_PROJECT_ID 
                and settings.FIREBASE_CLIENT_EMAIL 
                and settings.FIREBASE_PRIVATE_KEY
                and "YOUR_KEY_HERE" not in settings.FIREBASE_PRIVATE_KEY
            ):
                cred = credentials.Certificate({
                    "type": "service_account",
                    "project_id": settings.FIREBASE_PROJECT_ID,
                    "client_email": settings.FIREBASE_CLIENT_EMAIL,
                    "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
                })
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDK initialized with service account credentials.")
            else:
                logger.warning("Firebase credentials default/incomplete. Running Firebase auth in mock fallback mode.")
        except Exception as e:
            logger.warning(f"Firebase Admin SDK initialization bypassed ({e}). Running in dev mock mode.")

initialize_firebase()

async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    token = credentials.credentials if credentials else "dev_mock_token_12345"
    if firebase_admin._apps:
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except Exception as e:
            logger.warning(f"Live Firebase verification failed ({e}). Returning dev fallback user.")
            
    # Fallback mock decoded token for dev mode
    return {
        "uid": f"mock_user_{token[:10]}",
        "email": "demo@forgeai.dev",
        "phone_number": "+15550192834"
    }
