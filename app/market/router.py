from typing import Optional
from fastapi import APIRouter, HTTPException
from app.market.dao import MarketDAO

from fastapi_cache.decorator import cache

router = APIRouter(
  prefix="/market",
  tags=["Markets"]
)

@router.get("")
@cache(expire=90)
async def get_required_number_of_markets(limit = None):
  try:
    return await MarketDAO.find_limit_by_filter(limit=limit)
  except:
    raise HTTPException(status_code=400, detail="limit must be integer")


@router.get("/{id}")
async def get_market_by_id(id: int):
  if id > 0:
    return await MarketDAO.find_by_id(model_id= id)
  else:
    raise HTTPException(status_code=400, detail="must be positive id")


@router.get("/category/{category_id}")
@cache(expire=90)
async def get_markets_by_category(category_id: int, limit: Optional[int] = None):
  try:
    return await MarketDAO.find_limit_by_filter(limit=limit, category_id=category_id)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
