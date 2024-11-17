from sqladmin import ModelView

from app.category.model import Category
from app.market.model import Market
from app.orders.model import Order
from app.products.model import Product
from app.users.model import User


class UserAdmin(ModelView, model=User):
  column_list = [User.email, User.is_admin]
  name_plural = "Users"
  icon = "fa-solid fa-circle"
  column_details_exclude_list = [User.hashed_password, User.id]
  column_sortable_list = [User.is_admin]
  can_delete = False

class ProductAdmin(ModelView, model= Product):
  name_plural = "Products"
  icon = "fa-solid fa-circle"
  column_list = [Product.name, Product.price, Product.amount]
  column_details_exclude_list = [Product.id, Product.product_image_id, Product.category_id, Product.market_id]
  can_delete = False


class MarketAdmin(ModelView, model = Market):
  name_plural = "Markets"
  icon = "fa-solid fa-circle"
  column_list = [Market.name, Market.description]
  column_details_exclude_list = [Market.id, Market.category_id]
  can_delete = False


class OrderAdmin(ModelView, model=Order):
    name_plural = "Orders"
    icon = "fa-solid fa-circle"
    column_list = [
        Order.user_id,
        Order.quantity,
        Order.total_price,
        Order.is_paid,
        Order.adres,
    ]
    column_details_exclude_list = [Order.id, Order.market_id, Order.product_id, Order.user_id]
    column_sortable_list = [Order.is_paid]






class CategoryAdmin(ModelView, model=Category):
  name_plural = "Categories"
  icon = "fa-solid fa-circle"
  column_list = [Category.name]
  column_details_exclude_list = [Category.id]
