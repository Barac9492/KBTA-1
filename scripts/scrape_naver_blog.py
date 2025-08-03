#!/usr/bin/env python3
"""
K-Beauty Trend Scraper
Dynamic web scraper using Playwright to collect beauty content from Korean sources.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import re

from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup
import aiohttp
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KBeautyScraper:
    """Dynamic scraper for K-beauty content using Playwright."""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.output_file = self.data_dir / "scraped_content.json"
        
        # Target sources
        self.sources = {
            "naver_beauty": {
                "urls": [
                    "https://beauty.naver.com/",
                    "https://blog.naver.com/PostList.naver?blogId=beauty_naver",
                ],
                "selectors": {
                    "posts": "div.post_item, div.blog_post",
                    "title": "h3.title, h2.title",
                    "content": "div.content, div.post_content",
                    "date": "span.date, time",
                    "author": "span.author, a.author"
                }
            },
            "instagram_beauty": {
                "hashtags": [
                    "#kbeauty", "#koreanbeauty", "#koreanskincare",
                    "#kbeautytrends", "#koreanmakeup", "#koreancosmetics"
                ]
            },
            "youtube_beauty": {
                "channels": [
                    "https://www.youtube.com/@koreanbeauty",
                    "https://www.youtube.com/@kbeauty_trends"
                ]
            }
        }
        
        self.scraped_data = []
        
    async def init_browser(self) -> Browser:
        """Initialize Playwright browser."""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        return browser
    
    async def scrape_naver_beauty(self, page: Page) -> List[Dict]:
        """Scrape Naver Beauty content."""
        logger.info("Scraping Naver Beauty content...")
        scraped_posts = []
        
        for url in self.sources["naver_beauty"]["urls"]:
            try:
                await page.goto(url, wait_until="networkidle")
                await page.wait_for_timeout(2000)  # Wait for dynamic content
                
                # Scroll to load more content
                await self.scroll_page(page)
                
                # Extract posts
                posts = await page.query_selector_all(
                    self.sources["naver_beauty"]["selectors"]["posts"]
                )
                
                for post in posts[:20]:  # Limit to 20 posts per source
                    try:
                        post_data = await self.extract_post_data(post)
                        if post_data:
                            scraped_posts.append(post_data)
                    except Exception as e:
                        logger.warning(f"Error extracting post data: {e}")
                        
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                
        return scraped_posts
    
    async def scroll_page(self, page: Page):
        """Scroll page to load dynamic content."""
        for i in range(3):  # Scroll 3 times
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)
    
    async def extract_post_data(self, post_element) -> Optional[Dict]:
        """Extract data from a single post element."""
        try:
            # Extract title
            title_elem = await post_element.query_selector(
                self.sources["naver_beauty"]["selectors"]["title"]
            )
            title = await title_elem.text_content() if title_elem else "No title"
            
            # Extract content
            content_elem = await post_element.query_selector(
                self.sources["naver_beauty"]["selectors"]["content"]
            )
            content = await content_elem.text_content() if content_elem else "No content"
            
            # Extract date
            date_elem = await post_element.query_selector(
                self.sources["naver_beauty"]["selectors"]["date"]
            )
            date = await date_elem.text_content() if date_elem else "Unknown date"
            
            # Extract author
            author_elem = await post_element.query_selector(
                self.sources["naver_beauty"]["selectors"]["author"]
            )
            author = await author_elem.text_content() if author_elem else "Unknown author"
            
            # Get URL if available
            link_elem = await post_element.query_selector("a")
            url = await link_elem.get_attribute("href") if link_elem else None
            
            return {
                "title": title.strip(),
                "content": content.strip(),
                "date": date.strip(),
                "author": author.strip(),
                "url": url,
                "source": "naver_beauty",
                "scraped_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.warning(f"Error extracting post data: {e}")
            return None
    
    async def scrape_instagram_hashtags(self, page: Page) -> List[Dict]:
        """Scrape Instagram content using hashtags."""
        logger.info("Scraping Instagram beauty hashtags...")
        scraped_posts = []
        
        # Note: Instagram scraping requires authentication and may be rate-limited
        # This is a simplified version for demonstration
        for hashtag in self.sources["instagram_beauty"]["hashtags"]:
            try:
                url = f"https://www.instagram.com/explore/tags/{hashtag.replace('#', '')}/"
                await page.goto(url, wait_until="networkidle")
                await page.wait_for_timeout(3000)
                
                # Extract posts (Instagram structure may vary)
                posts = await page.query_selector_all("article a")
                
                for post in posts[:10]:  # Limit to 10 posts per hashtag
                    try:
                        post_url = await post.get_attribute("href")
                        if post_url:
                            scraped_posts.append({
                                "title": f"Instagram post - {hashtag}",
                                "content": f"Instagram content from {hashtag}",
                                "url": f"https://www.instagram.com{post_url}",
                                "source": "instagram",
                                "hashtag": hashtag,
                                "scraped_at": datetime.now().isoformat()
                            })
                    except Exception as e:
                        logger.warning(f"Error extracting Instagram post: {e}")
                        
            except Exception as e:
                logger.error(f"Error scraping Instagram hashtag {hashtag}: {e}")
                
        return scraped_posts
    
    async def scrape_youtube_beauty(self, page: Page) -> List[Dict]:
        """Scrape YouTube beauty content."""
        logger.info("Scraping YouTube beauty content...")
        scraped_posts = []
        
        for channel_url in self.sources["youtube_beauty"]["channels"]:
            try:
                await page.goto(channel_url, wait_until="networkidle")
                await page.wait_for_timeout(2000)
                
                # Extract video titles and descriptions
                videos = await page.query_selector_all("a#video-title")
                
                for video in videos[:15]:  # Limit to 15 videos per channel
                    try:
                        title = await video.get_attribute("title")
                        url = await video.get_attribute("href")
                        
                        if title and url:
                            scraped_posts.append({
                                "title": title,
                                "content": f"YouTube video: {title}",
                                "url": f"https://www.youtube.com{url}",
                                "source": "youtube",
                                "scraped_at": datetime.now().isoformat()
                            })
                    except Exception as e:
                        logger.warning(f"Error extracting YouTube video: {e}")
                        
            except Exception as e:
                logger.error(f"Error scraping YouTube channel {channel_url}: {e}")
                
        return scraped_posts
    
    async def scrape_all_sources(self):
        """Scrape content from all configured sources."""
        browser = await self.init_browser()
        
        try:
            page = await browser.new_page()
            
            # Set user agent to avoid detection
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            # Scrape from different sources
            naver_data = await self.scrape_naver_beauty(page)
            instagram_data = await self.scrape_instagram_hashtags(page)
            youtube_data = await self.scrape_youtube_beauty(page)
            
            # Combine all scraped data
            self.scraped_data = naver_data + instagram_data + youtube_data
            
            logger.info(f"Successfully scraped {len(self.scraped_data)} posts")
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
        finally:
            await browser.close()
    
    def save_data(self):
        """Save scraped data to JSON file."""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "scraped_at": datetime.now().isoformat(),
                    "total_posts": len(self.scraped_data),
                    "posts": self.scraped_data
                }, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Data saved to {self.output_file}")
            
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def filter_relevant_content(self) -> List[Dict]:
        """Filter content for K-beauty relevance."""
        kbeauty_keywords = [
            "korean", "k-beauty", "kbeauty", "skincare", "beauty",
            "cosmetics", "makeup", "skincare", "serum", "essence",
            "toner", "moisturizer", "cleanser", "mask", "cream",
            "korean beauty", "korean skincare", "korean makeup"
        ]
        
        relevant_posts = []
        
        for post in self.scraped_data:
            content_text = f"{post.get('title', '')} {post.get('content', '')}".lower()
            
            # Check if post contains K-beauty related keywords
            if any(keyword in content_text for keyword in kbeauty_keywords):
                relevant_posts.append(post)
        
        logger.info(f"Filtered to {len(relevant_posts)} relevant posts")
        return relevant_posts

async def main():
    """Main function to run the scraper."""
    scraper = KBeautyScraper()
    
    logger.info("Starting K-beauty content scraping...")
    
    # Scrape all sources
    await scraper.scrape_all_sources()
    
    # Filter for relevant content
    relevant_content = scraper.filter_relevant_content()
    
    # Update scraped data with filtered content
    scraper.scraped_data = relevant_content
    
    # Save data
    scraper.save_data()
    
    logger.info("Scraping completed successfully!")

if __name__ == "__main__":
    asyncio.run(main()) 