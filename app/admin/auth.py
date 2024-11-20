from datetime import datetime, timedelta, timezone
import jwt
from starlette.responses import RedirectResponse
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend
from app.users.auth import verify_password

from app.config import settings

from fastapi import Depends, HTTPException, status

from app.users.auth import create_token
from app.users.dao import UserDAO



class AdminAuth(AuthenticationBackend):

  async def login(self, request: Request):

    form = await request.form()
    email, password = form["username"], form["password"]


    try:
      admin = await UserDAO.find_one_or_none(email=email)

      if not admin:
        return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

      if not verify_password(password, admin.hashed_password):
        return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

      admin_access_token = create_token(time_to_exp=30, data={"sub": str(admin.id), "role": "admin"})
      request.session.update({"token": admin_access_token})
      return True

    except:
      RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

  @staticmethod
  def get_token(request: Request) -> str:
    token = request.cookies.get("session") or request.session.get("token")
    if not token:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
    return token

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

authenication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
