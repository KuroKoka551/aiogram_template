from datetime import timedelta

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka

from aiogram_template.config import Config
from aiogram_template.di.providers import ContextProvider, DatabaseProvider
from aiogram_template.runners import on_shutdown, on_startup
from aiogram_template.utils import mjson


def _setup_middlewares(dp: Dispatcher, config: Config) -> None:
    """
    Setup middlewares for dispatcher

    :param dp: Dispatcher instance
    :param config: Application config

    :return: None
    """
    dp["main_container"] = container = AsyncContainer(
        DatabaseProvider(), ContextProvider(), context={Config: config}
    )
    setup_dishka(container, dp)
    setup_dialogs(dp)


def setup_dispatcher(config: Config) -> Dispatcher:
    """
    Setup dispatcher with installed middlewares and included routers

    :param config: Application config

    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """

    storage = RedisStorage.from_url(
        url=config.redis_url,
        json_loads=mjson.decode,
        json_dumps=mjson.encode,
        key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True),
        state_ttl=timedelta(days=35),
        data_ttl=timedelta(days=35),
    )
    dp = Dispatcher(
        storage=storage,
        events_isolation=storage.create_isolation(),
        config=config,
    )
    _setup_middlewares(dp, config)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return dp
