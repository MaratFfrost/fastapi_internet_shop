from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.products.dao import ProductDAO


router = APIRouter(
  prefix="/product",
  tags=["Product"]
)


@router.get("/{id}")
async def get_product_by_id(id: int):
  if id <= 0:
    raise HTTPException(status_code=400, detail="id must be positive")
  return await ProductDAO.find_by_id(model_id=id)


@router.post("/by_market-category")
async def get_all_product_from_market_or_category(
    category_id: int = Query(None),
    market_id: int = Query(None),
    limit: Optional[int] = None
):
    try:
        return await ProductDAO.find_limit_by_filter(
             limit=limit,
             category_id=category_id,
             market_id=market_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
