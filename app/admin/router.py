from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.admin.auth import AdminAuth
from app.users.model import User

router = APIRouter(
  prefix="/report_for_admin",
  tags=["Admin"]
)
