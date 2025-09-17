import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

from src.bot.config import bot, logger
from src.bot.handlers import news

dp = Dispatcher()

async def main():
    logger.info("Bot started")
    dp.include_routers(news.router)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
