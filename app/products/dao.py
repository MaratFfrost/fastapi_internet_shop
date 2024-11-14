from app.dao.base import BaseDAO
from app.products.model import Product

class ProductDAO(BaseDAO):
  model = Product
