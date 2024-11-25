from fastapi import APIRouter, Depends, HTTPException

from app.products.dao import ProductDAO
from app.reviews.schemas import SReviews
from app.users.dependencies import get_current_user
from app.users.model import User

router = APIRouter(
  prefix="/reviews",
  tags=["Review"]
)

@router.post("/show")
async def show_reviws(data: SReviews):
  product = await ProductDAO.find_one_or_none(id = data.product_id)

  if not product:
    raise HTTPException(status_code=404, detail="such product doesn`t exist")






@router.post("write")
async def write_reviws(data: SReviews, user: User = Depends(get_current_user)):
  product = await ProductDAO.find_one_or_none(id = data.product_id)

  if not product:
    raise HTTPException(status_code=404, detail="such product doesn`t exist")


@router.delete("delete/{reviews_id}")
async def delete_reviws(reviews_id: int, user: User = Depends(get_current_user)):
  pass
