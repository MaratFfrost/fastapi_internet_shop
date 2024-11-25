from datetime import datetime, timezone
from fastapi import Depends, HTTPException, Request, status
import jwt
from app.config import settings

from app.users.dao import UserDAO


def get_token(request: Request) -> str:
    token = request.cookies.get("session") or request.session.get("token")
    if not token:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
    return token


async def get_current_admin(token: str = Depends(get_token)):
    try:

      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SECRET_ALGORITHM])

    except Exception as e:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    expire = payload.get("exp")
    if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    admin_id = payload.get("sub")
    role = payload.get("role")

    if not admin_id or role != "admin":
      raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    admin = await UserDAO.find_one_or_none(id = int(admin_id))

    if not admin.is_admin:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return admin
