from app.dao.base import BaseDAO
from app.users.model import User
from app.users.shemas import SUserLogin

class UserDAO(BaseDAO):
  model = User
