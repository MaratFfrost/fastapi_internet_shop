from datetime import datetime, timedelta, timezone
import jwt
from starlette.responses import RedirectResponse
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend

from app.config import settings

from fastapi import Depends, HTTPException, status

from app.users.dao import UserDAO

class AdminAuth(AuthenticationBackend):

  async def login(self, request: Request):
    form = await request.form()
    email, password = form["username"], form["password"]

    admin = await UserDAO.find_one_or_none(email=email, hashed_password=password)

    if not admin:
        return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

    admin_access_token = self.create_admin_access_token({"sub": str(admin.id)})
    request.session.update({"token": admin_access_token})
    return True

  @staticmethod
  def get_token(request: Request) -> str:
    token = request.cookies.get("session") or request.session.get("token")
    if not token:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
    return token

  @staticmethod
  def create_admin_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire, "role": "admin"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.SECRET_ALGORITHM
    )
    return encoded_jwt

  async def get_current_admin(self, token: str = Depends(get_token)):
    try:
      payload = jwt.decode(token, settings.SECRET_KEY, settings.SECRET_ALGORITHM)
    except jwt.PyJWTError:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")

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


  async def logout(self, reqest: Request):
    reqest.session.clear()
    return True

  async def authenticate(self, request: Request) -> bool:
    token = request.session.get("token")

    if not token:
      return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

    try:
      await self.get_current_admin(token)
    except HTTPException:
      return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

    return True

authenication_backend = AdminAuth(secret_key="...")
