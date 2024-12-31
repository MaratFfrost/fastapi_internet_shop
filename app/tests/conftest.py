import asyncio
from httpx import AsyncClient
import pytest
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app


from users.model import User
from category.model import Category
from market.model import Market
from products.model import Product
from orders.model import Order


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        try:
            print("Dropping all tables...")
            await conn.run_sync(Base.metadata.drop_all)
            print("Clearing metadata...")
            Base.metadata.clear()
            print("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error while preparing the database: {e}")
            raise



@pytest.fixture(scope="session")
def event_loop(request):
  loop = asyncio.get_event_loop_policy().new_event_loop()
  yield loop
  loop.close()

@pytest.fixture(scope="function")
async def ac():
  async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
    yield ac
