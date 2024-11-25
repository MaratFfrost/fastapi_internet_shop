from datetime import datetime, timedelta, timezone
import jwt
from starlette.responses import RedirectResponse
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend
from app.admin.dependencies import get_current_admin
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

  async def logout(self, reqest: Request):
    reqest.session.clear()
    return True

  async def authenticate(self, request: Request) -> bool:
    token = request.session.get("token")

    if not token:
      return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

    try:
      await get_current_admin(token)
    except HTTPException:
      return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

    return True

authenication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
