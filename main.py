import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
from src.database import init_db
from src.handlers import registration, schedule, admin


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    db = await init_db()

    dp.include_routers(
        registration.router,
        schedule.router,
        admin.router,
    )

    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
