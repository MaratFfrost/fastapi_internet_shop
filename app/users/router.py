from fastapi import APIRouter, Depends, HTTPException, Response, status

from fastapi_cache.decorator import cache

from app.orders.dao import OrderDAO
from app.products.dao import ProductDAO
from app.users.auth import authencicate_user, create_access_token, get_password_hash
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
async def make_order(user_data: SUserOrder ,user: User = Depends(get_current_user)):
    if user_data.quantity <= 0 or len(user_data.adres) == 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="quantity of product must be greater zero or  adress must not be empty")


    product = await ProductDAO.find_one_or_none(id = user_data.product_id)

    if not product:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product wasn`t found")

    if product.amount < user_data.quantity:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="impossible to make order because of a big quantity of product")

    ful_price = user_data.quantity * product.price


    await OrderDAO.add(
                       user_id = user.id,
                       market_id = user_data.market_id,
                       product_id = user_data.product_id,
                       quantity = user_data.quantity,
                       total_price = ful_price,
                       is_paid = False,
                       adres = user_data.adres
                       )

    return "order was added cart"


@router.delete("/del_an_order")
async def delete_order(order_id: int, user: User = Depends(get_current_user)):
  try:
    await OrderDAO.delete_by_filters(id = order_id)
    return "order was deleted"
  except Exception as e:
    HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/register")
async def register(user_data: SUserLogin):
    user = await UserDAO.find_one_or_none(email = user_data.email)
    if user:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exist")
    password = get_password_hash(user_data.password)
    await UserDAO.add(email = user_data.email, hashed_password = password, is_admin=False)
    return f"added sucsessfuly"


@router.post("/login")
async def login( response: Response, user_data: SUserLogin):

   user = await authencicate_user(user_data.email, user_data.password)
   if not user:
     raise HTTPException(status_code=401)
   access_token = create_access_token({"sub":str(user.id)})
   response.set_cookie("booking_access_token", access_token, httponly=True, secure=True,)
   return "user login sucsesful"


@router.post("/logout")
async def logout(response: Response, user: User = Depends(get_current_user)):
  try:
    response.delete_cookie("booking_access_token")
    return f"You logout sucsesful"
  except:
    raise HTTPException(status_code=400)


@router.delete("/delete_account")
async def delete_user(response: Response, user: User = Depends(get_current_user)):
  try:
    await UserDAO.delete_by_filters(id = user.id)
    response.delete_cookie("booking_access_token")
    return f"account deleted sucsessfuly"
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
