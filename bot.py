import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config_data.config import Config, load_config
from handlers.other import register_other_handlers
from handlers.user import register_user_handlers
from handlers.user_reg import register_reg_handlers
from handlers.admin import register_admin_handlers
from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)
storage = MemoryStorage()


def register_all_handlers(dp: Dispatcher) -> None:
    register_reg_handlers(dp)
    register_user_handlers(dp)
    register_admin_handlers(dp)
    register_other_handlers(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config(r'.env')

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(bot, storage=storage)

    await set_main_menu(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')