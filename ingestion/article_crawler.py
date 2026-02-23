import feedparser 
import pandas as pd 
from newspaper import Article 
from datetime import datetime 
import time 
import random 
import nltk
import requests
from bs4 import BeautifulSoup
import re

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')


class Crawler: 
    def __init__(self):
        self.feeds = {
            # --- CAFE F ---
            
            "cafeF_stock": "https://cafef.vn/thi-truong-chung-khoan.rss",
            "cafeF_bank": "https://cafef.vn/tai-chinh-ngan-hang.rss",
            "cafeF_real_estate": "https://cafef.vn/bat-dong-san.rss",
            "cafeF_business": "https://cafef.vn/doanh-nghiep.rss",
            "cafeF_crypto": "https://cafef.vn/smart-money.rss",
            "cafeF_international":"https://cafef.vn/tai-chinh-quoc-te.rss",
            "cafeF_economy": "https://cafef.vn/kinh-te-so.rss",
            "cafeF_market": "https://cafef.vn/thi-truong.rss",
            "cafeF_macro": "https://cafef.vn/vi-mo-dau-tu.rss",
            
             # --- VIETSTOCK ---
            "vietstock_market": "https://vietstock.vn/chung-khoan.htm",
            "vietstock_corp": "https://vietstock.vn/doanh-nghiep.htm",
            "vietstock_real_estate": "https://vietstock.vn/bat-dong-san.htm",
            "vietstock_finance": "https://vietstock.vn/tai-chinh.htm",
            "vietstock_commodities":"https://vietstock.vn/hang-hoa.htm",
            "vietstock_economy":"https://vietstock.vn/kinh-te.htm",
            "vietstock_world":"https://vietstock.vn/the-gioi.htm",
            "vietstock_personal_finance":"https://vietstock.vn/tai-chinh-ca-nhan.htm",
            "vietstock_analysis":"https://vietstock.vn/nhan-dinh-phan-tich.htm",
            "vietstock_indochina":"https://vietstock.vn/dong-duong.htm",
            
            # --- VNEXPRESS ---
            "vnexpress_business": "https://vnexpress.net/rss/kinh-doanh.rss"

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
        if url.endswith(".rss"):
            feed = feedparser.parse(url)
            for entry in feed.entries:
                articles.append({
                    "title": entry.title,
                    "url": entry.link,
                    "published_at": entry.get('published', ''),
                    "category": category,
                })
        elif url.endswith(".htm"):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                seen_links = set()
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    title = a_tag.get('title') or a_tag.get_text(strip=True)
                    if href.endswith('.htm') and re.search(r'/\d{4}/\d{2}/', href):
                        if href.startswith('/'):
                            full_url = f"https://vietstock.vn{href}"
                        elif href.startswith('http'):
                            full_url = href
                        else:
                            full_url = f"https://vietstock.vn/{href}"
                        if full_url not in seen_links and len(title) > 10:
                            seen_links.add(full_url)
                            articles.append({
                                "title": title,
                                "url": full_url,
                                "published_at": "",
                                "category": category,
                            })
            except Exception as e:
                print(f"Error from {url}: {e}")

        return articles 
    
    def parse_content(self, url):
        try: 
            article = Article(url)
            article.download()
            article.parse()
            article.nlp() 
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
    def scrape(self):
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
    bot = Crawler()
    df = bot.scrape()
    filename = f"article_data_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} articles to {filename}")
