import asyncio
import logging
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app import db
from app.arguments import parse_arguments
from app.config import Config, parse_config
from app.db import close_orm, init_orm
from app.files.logs_logic import SimpleLogging
from app.handlers import get_handlers_router
from app.middlewares import register_middlewares
from app.commands import remove_bot_commands, setup_bot_commands


async def on_startup(dispatcher: Dispatcher, bot: Bot, config: Config):
    await register_middlewares(dp=dispatcher)

    dispatcher.include_router(get_handlers_router())

    await setup_bot_commands(bot, config)
    await bot.delete_webhook(
        drop_pending_updates=config.settings.drop_pending_updates,
    )

    tortoise_config = config.database.get_tortoise_config()
    await init_orm(tortoise_config)

    bot_info = await bot.get_me()

    logging.info(f"Name - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID - {bot_info.id}")

    logging.error("Bot started!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot, config: Config):
    logging.warning("Stopping bot...")
    await remove_bot_commands(bot, config)
    await bot.delete_webhook(drop_pending_updates=config.settings.drop_pending_updates)
    await dispatcher.fsm.storage.close()
    await bot.session.close()
    await close_orm()


async def main():
    logging.basicConfig(level=logging.INFO,
                        format=SimpleLogging.logs_format,
                        handlers=SimpleLogging.get_handlers()
                        )

    arguments = parse_arguments()
    config = parse_config(arguments.config)

    tortoise_config = config.database.get_tortoise_config()
    try:
        await db.create_models(tortoise_config)
    except FileExistsError:
        await db.migrate_models(tortoise_config)

    bot_token = config.bot.token

    bot = Bot(bot_token, parse_mode="HTML")
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot, dp=dp, config=config)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
