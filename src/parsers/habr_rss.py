import aiohttp
import feedparser
from typing import List, Dict

class HabrRSSParser:
    BASE_URL = "https://habr.com/ru/rss/hubs/"

    async def fetch_rss(self, category: str) -> str:
        url = f"{self.BASE_URL}{category}/articles/all"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()

    async def fetch_latest(self, category: str, count: int = 5) -> List[Dict]:
        rss_text = await self.fetch_rss(category)
        feed = feedparser.parse(rss_text)
        articles = []
        for entry in feed.entries[:count]:
            articles.append({
                "title": entry.title,
                "url": entry.link,
                "categories": [tag.term for tag in getattr(entry, 'tags', [])],
                "published": entry.published
            })
        return articles

