import asyncio
import logging
import signal

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

from src.bot.config import settings, bot, logger, sub_service
from src.bot.handlers import news
from src.bot.scheduler import setup_scheduler

dp = Dispatcher()


async def main():
    setup_scheduler()
    dp.include_routers(news.router)

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
