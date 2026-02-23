import feedparser 
import pandas as pd 
from newspaper import Article 
from datetime import datetime 
import time 
import random 
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class CafeCrawler: 
    def __init__(self):
        self.feeds = {
            "stock": "https://cafef.vn/thi-truong-chung-khoan.rss",
            'bank': "https://cafef.vn/tai-chinh-ngan-hang.rss",
            'real_estate': "https://cafef.vn/bat-dong-san.rss",
            'business': "https://cafef.vn/doanh-nghiep.rss",
            'crypto': "https://cafef.vn/smart-money.rss",
            "international":"https://cafef.vn/tai-chinh-quoc-te.rss",
            "economy": "https://cafef.vn/kinh-te-so.rss",
            "market": "https://cafef.vn/thi-truong.rss",
            "macro": "https://cafef.vn/vi-mo-dau-tu.rss"

        }
          # Fake header to look like a real browser (Anti-blocking)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    def fetch_articles(self, category):
        url = self.feeds.get(category)
        if not url:
            print(f"Category {category} not found")
            return []
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            articles.append({
                "title": entry.title,
                "url": entry.link,
                "published_at": entry.published,
                "category": category,
            })
        return articles 
    def parse_content(self, url):
        try: 
            article = Article(url)
            article.download()
            article.parse()
            return {
                "full_text":article.text,
                "author": article.authors,
                "top_image": article.top_image,
                "keywords": article.keywords,
                "summary": article.summary
            }
        except Exception as e:
            print(f"Error parsing article {url}: {e}")
            return None
    def crawl(self):
        all_data = []
        for category in self.feeds:
            links = self.fetch_articles(category)
            print(f"Fetched {len(links)} articles for category {category}")
            for link in links[:3]:
                content = self.parse_content(link['url'])
                if content: 
                    full_record = {**link, **content, "crawled_at": datetime.now().isoformat()}
                    all_data.append(full_record)
                time.sleep(random.uniform(1,3))
        return pd.DataFrame(all_data)
if __name__ == "__main__":
    bot = CafeCrawler()
    df = bot.crawl()
    filename = f"cafef_data_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} articles to {filename}")
