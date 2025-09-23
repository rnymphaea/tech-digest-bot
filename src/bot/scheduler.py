import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.bot.config import bot, sub_service, parser, settings

sent_articles = set()


async def send_articles():
    categories = sub_service.get_all_categories()

    for category in categories:
        try:
            articles = await parser.fetch_latest(category, count=3)
        except Exception as e:
            logger.error(f"Ошибка при парсинге категории {category}: {e}")
            continue

        for article in articles:
            if article["url"] in sent_articles:
                continue

            users = sub_service.get_category_users(category)
            if not users:
                continue

            text = (
                f"📌 <b>{article['title']}</b>\n\n"
                f"📂 Категории: <i>{', '.join(article.get('categories', []))}</i>\n\n"
                f"⏱️ Дата публикации: {article['published']}\n\n"
                f"Ссылка: {article['url']}\n\n"
            )

            for user_id in users:
                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text=text,
                        parse_mode="HTML"
                    )
                except Exception as e:
                    logger.warning(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

            sent_articles.add(article["url"])


def setup_scheduler():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_articles, "interval", minutes=settings.timeout_minutes)
    scheduler.start()
