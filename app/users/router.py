import json
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from fastapi_cache.decorator import cache

from random import randint

import jwt

from app.config import settings

from app.orders.dao import OrderDAO
from app.products.dao import ProductDAO
from app.services.consumer import send_email_to_user
from app.services.producer import send_to_rabbitmq
from app.users.auth import activate, authencicate_user, create_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.model import User
from app.users.shemas import SUserLogin, SUserOrder

router = APIRouter(
  prefix="/user",
  tags=["Users"]
)



@router.get("/my_orders")
@cache(expire=65)
async def show_orders(user: User = Depends(get_current_user)):
  try:
    return await OrderDAO.find_limit_by_filter(user_id = user.id)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/make_an_order")
async def make_order(user_data: SUserOrder, user: User = Depends(get_current_user)):
    if user_data.quantity <= 0 or not user_data.adres.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero, and address must not be empty"
        )

    product = await ProductDAO.find_one_or_none(id=user_data.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product.amount < user_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough products in stock"
        )

    total_price = product.price * user_data.quantity
    await OrderDAO.add(
        user_id=user.id,
        market_id=user_data.market_id,
        product_id=user_data.product_id,
        quantity=user_data.quantity,
        total_price=total_price,
        is_paid=False,
        adres=user_data.adres
    )
    return {"message": "Order successfully created"}



@router.delete("/del_an_order")
async def delete_order(order_id: int, user: User = Depends(get_current_user)):
  try:
    await OrderDAO.delete_by_filters(id = order_id)
    return "order was deleted"
  except Exception as e:
    HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/register")
async def register(response: Response , user_data: SUserLogin):
    user = await UserDAO.find_one_or_none(email = user_data.email)
    if user:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exist")
    code = randint(10000, 99999)

    password = get_password_hash(user_data.password)
    data_token = create_token( time_to_exp=10, data={"code":code, "email":f"{user_data.email}", "password": password})

    response.set_cookie("data", data_token, httponly=True, secure=True)
    message = {
        "email": user_data.email,
        "code": code
    }
    message_body = json.dumps(message)
    send_to_rabbitmq(message_body)
    send_email_to_user()

    return f"code was sent"



@router.post("/activate_account")
async def activate_account(request: Request, code_user: int):

    token = request.cookies.get("data")
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found")

    try:
      result = await activate(token=token, code_user=code_user)
    except:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    await UserDAO.add(email=result[0], hashed_password=result[1], is_admin=False )

    return {"message": "User added successfully"}





@router.post("/login")
async def login(response: Response, user_data: SUserLogin):

   user = await authencicate_user(user_data.email, user_data.password)
   if not user:
     raise HTTPException(status_code=401)
   access_token = create_token(time_to_exp=30, data={"sub":str(user.id)})
   response.set_cookie("access_token", access_token, httponly=True, secure=True,)
   return "user login sucsesful"


@router.post("/logout")
async def logout(response: Response, user: User = Depends(get_current_user)):
  try:
    response.delete_cookie("access_token")
    return f"You logout sucsesful"
  except:
    raise HTTPException(status_code=400)


@router.delete("/delete_account")
async def delete_user(response: Response, user: User = Depends(get_current_user)):
  try:
    await OrderDAO.delete_by_filters(user_id = user.id)
    await UserDAO.delete_by_filters(id = user.id)
    response.delete_cookie("access_token")
    return f"account deleted sucsessfuly"
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
