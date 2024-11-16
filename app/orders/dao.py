from app.dao.base import BaseDAO
from app.orders.model import Order

class OrderDAO(BaseDAO):
  model = Order
