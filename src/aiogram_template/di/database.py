from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from aiogram_template.config import PostgresConfig


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, db_config: PostgresConfig) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(db_config.url)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def get_session(self, engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
        async with AsyncSession(bind=engine, expire_on_commit=False) as session:
            yield session
