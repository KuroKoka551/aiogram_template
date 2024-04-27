import logging

from aiogram_template.config import Config
from aiogram_template.factories import create_bot, setup_dispatcher
from aiogram_template.runner import run_webhook


def main() -> None:
    config = Config.create()
    bot = create_bot(config)
    dp = setup_dispatcher(config)
    if config.webhook.use:
        run_webhook(dp, config, bot)
    dp.run_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(name)s - %(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    main()
