from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.security import verify_token

# Rate limiter based on IP address
limiter = Limiter(key_func=get_remote_address)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/guest")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload.get("sub")