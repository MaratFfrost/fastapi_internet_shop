from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.admin.views import CategoryAdmin, MarketAdmin, OrderAdmin, ProductAdmin, UserAdmin
from app.market.router import router as market_router
from app.products.router import router as product_router
from app.users.router import router as user_router
from app.config import settings
from app.database import engine
from app.admin.auth import authenication_backend

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()

app = FastAPI(lifespan=lifespan)

origins = ["*"] #но не рекомендуется отсавлять все так как любой может подключиться к апи

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_router)
app.include_router(product_router)
app.include_router(user_router)


admin = Admin(app, engine, authentication_backend=authenication_backend)

admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)
admin.add_view(MarketAdmin)
admin.add_view(OrderAdmin)
admin.add_view(CategoryAdmin)
