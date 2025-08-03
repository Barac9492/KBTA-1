"""
Modular scraper for K-Beauty content collection
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import os

from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup
import aiohttp

from core.config import config
from core.models import ScrapedPost

logger = logging.getLogger(__name__)

class KBeautyScraper:
    """Modular scraper for K-beauty content."""
    
    def __init__(self):
        self.config = config.scraping
        self.sources_config = config.get_sources_config()
        self.scraped_posts: List[ScrapedPost] = []
        
    async def init_browser(self) -> Browser:
        """Initialize Playwright browser."""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=self.config.headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        return browser
    
    async def scrape_all_sources(self) -> List[ScrapedPost]:
        """Scrape content from all configured sources."""
        logger.info("Starting K-beauty content scraping...")
        
        # Check if we're in test mode
        if os.getenv("TEST_MODE", "false").lower() == "true":
            logger.info("Running in test mode with mock data")
            return self._generate_mock_data()
        
        browser = await self.init_browser()
        
        try:
            page = await browser.new_page()
            
            # Set user agent
            await page.set_extra_http_headers({
                "User-Agent": self.config.user_agent
            })
            
            # Scrape from different sources
            naver_posts = await self._scrape_naver_beauty(page)
            instagram_posts = await self._scrape_instagram_hashtags(page)
            youtube_posts = await self._scrape_youtube_beauty(page)
            
            # Combine all scraped data
            self.scraped_posts = naver_posts + instagram_posts + youtube_posts
            
            # Filter for relevance
            relevant_posts = self._filter_relevant_content()
            
            logger.info(f"Successfully scraped {len(relevant_posts)} relevant posts")
            return relevant_posts
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            return []
        finally:
            await browser.close()
    
    async def _scrape_naver_beauty(self, page: Page) -> List[ScrapedPost]:
        """Scrape Naver Beauty content."""
        logger.info("Scraping Naver Beauty content...")
        scraped_posts = []
        
        naver_config = self.sources_config["naver_beauty"]
        
        for url in naver_config["urls"]:
            try:
                await page.goto(url, wait_until="networkidle", timeout=self.config.timeout)
                await page.wait_for_timeout(2000)
                
                # Scroll to load more content
                await self._scroll_page(page)
                
                # Extract posts
                posts = await page.query_selector_all(naver_config["selectors"]["posts"])
                
                for post in posts[:self.config.max_posts_per_source]:
                    try:
                        post_data = await self._extract_post_data(post, naver_config["selectors"])
                        if post_data:
                            scraped_posts.append(post_data)
                    except Exception as e:
                        logger.warning(f"Error extracting post data: {e}")
                        
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                
        return scraped_posts
    
    async def _scrape_instagram_hashtags(self, page: Page) -> List[ScrapedPost]:
        """Scrape Instagram content using hashtags."""
        logger.info("Scraping Instagram beauty hashtags...")
        scraped_posts = []
        
        instagram_config = self.sources_config["instagram_beauty"]
        
        for hashtag in instagram_config["hashtags"]:
            try:
                url = f"https://www.instagram.com/explore/tags/{hashtag.replace('#', '')}/"
                await page.goto(url, wait_until="networkidle", timeout=self.config.timeout)
                await page.wait_for_timeout(3000)
                
                # Extract posts (Instagram structure may vary)
                posts = await page.query_selector_all("article a")
                
                for post in posts[:10]:  # Limit to 10 posts per hashtag
                    try:
                        post_url = await post.get_attribute("href")
                        if post_url:
                            scraped_posts.append(ScrapedPost(
                                title=f"Instagram post - {hashtag}",
                                content=f"Instagram content from {hashtag}",
                                source="instagram",
                                url=f"https://www.instagram.com{post_url}",
                                scraped_at=datetime.now()
                            ))
                    except Exception as e:
                        logger.warning(f"Error extracting Instagram post: {e}")
                        
            except Exception as e:
                logger.error(f"Error scraping Instagram hashtag {hashtag}: {e}")
                
        return scraped_posts
    
    async def _scrape_youtube_beauty(self, page: Page) -> List[ScrapedPost]:
        """Scrape YouTube beauty content."""
        logger.info("Scraping YouTube beauty content...")
        scraped_posts = []
        
        youtube_config = self.sources_config["youtube_beauty"]
        
        for channel_url in youtube_config["channels"]:
            try:
                await page.goto(channel_url, wait_until="networkidle", timeout=self.config.timeout)
                await page.wait_for_timeout(2000)
                
                # Extract video titles and descriptions
                videos = await page.query_selector_all("a#video-title")
                
                for video in videos[:15]:  # Limit to 15 videos per channel
                    try:
                        title = await video.get_attribute("title")
                        url = await video.get_attribute("href")
                        
                        if title and url:
                            scraped_posts.append(ScrapedPost(
                                title=title,
                                content=f"YouTube video: {title}",
                                source="youtube",
                                url=f"https://www.youtube.com{url}",
                                scraped_at=datetime.now()
                            ))
                    except Exception as e:
                        logger.warning(f"Error extracting YouTube video: {e}")
                        
            except Exception as e:
                logger.error(f"Error scraping YouTube channel {channel_url}: {e}")
                
        return scraped_posts
    
    async def _scroll_page(self, page: Page):
        """Scroll page to load dynamic content."""
        for i in range(3):  # Scroll 3 times
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)
    
    async def _extract_post_data(self, post_element, selectors: Dict) -> Optional[ScrapedPost]:
        """Extract data from a single post element."""
        try:
            # Extract title
            title_elem = await post_element.query_selector(selectors["title"])
            title = await title_elem.text_content() if title_elem else "No title"
            
            # Extract content
            content_elem = await post_element.query_selector(selectors["content"])
            content = await content_elem.text_content() if content_elem else "No content"
            
            # Extract date
            date_elem = await post_element.query_selector(selectors["date"])
            date = await date_elem.text_content() if date_elem else "Unknown date"
            
            # Extract author
            author_elem = await post_element.query_selector(selectors["author"])
            author = await author_elem.text_content() if author_elem else "Unknown author"
            
            # Get URL if available
            link_elem = await post_element.query_selector("a")
            url = await link_elem.get_attribute("href") if link_elem else None
            
            return ScrapedPost(
                title=title.strip(),
                content=content.strip(),
                source="naver_beauty",
                url=url,
                author=author.strip(),
                date=date.strip()
            )
            
        except Exception as e:
            logger.warning(f"Error extracting post data: {e}")
            return None
    
    def _filter_relevant_content(self) -> List[ScrapedPost]:
        """Filter content for K-beauty relevance."""
        kbeauty_keywords = [
            "korean", "k-beauty", "kbeauty", "skincare", "beauty",
            "cosmetics", "makeup", "skincare", "serum", "essence",
            "toner", "moisturizer", "cleanser", "mask", "cream",
            "korean beauty", "korean skincare", "korean makeup",
            "k-beauty", "kbeauty", "korean cosmetics"
        ]
        
        relevant_posts = []
        
        for post in self.scraped_posts:
            content_text = f"{post.title} {post.content}".lower()
            
            # Check if post contains K-beauty related keywords
            if any(keyword in content_text for keyword in kbeauty_keywords):
                relevant_posts.append(post)
        
        logger.info(f"Filtered to {len(relevant_posts)} relevant posts")
        return relevant_posts
    
    def save_scraped_data(self, posts: List[ScrapedPost], output_file: Path):
        """Save scraped data to JSON file."""
        try:
            data = {
                "scraped_at": datetime.now().isoformat(),
                "total_posts": len(posts),
                "posts": [post.to_dict() for post in posts]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                import json
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Data saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving data: {e}")

    def _generate_mock_data(self) -> List[ScrapedPost]:
        """Generate mock data for testing."""
        mock_posts = [
            ScrapedPost(
                title="2024년 K뷰티 트렌드: 글래스 스킨 메이크업",
                content="올해 가장 인기 있는 K뷰티 트렌드는 글래스 스킨 메이크업입니다. 투명하고 촉촉한 피부 표현이 핵심이며, 셀럽들도 이 트렌드를 적극 활용하고 있습니다.",
                source="naver_beauty",
                url="https://example.com/glass-skin-trend",
                date=datetime.now(),
                author="K뷰티 전문가"
            ),
            ScrapedPost(
                title="한국 화장품 브랜드 신상품 리뷰",
                content="새로 출시된 한국 화장품 브랜드들의 제품들을 리뷰해보았습니다. 특히 스킨케어 제품들의 품질이 매우 우수하며, 해외에서도 큰 인기를 얻고 있습니다.",
                source="instagram_beauty",
                url="https://example.com/korean-cosmetics-review",
                date=datetime.now(),
                author="뷰티 인플루언서"
            ),
            ScrapedPost(
                title="K뷰티 메이크업 튜토리얼",
                content="한국식 메이크업 기법을 활용한 데일리 메이크업 튜토리얼입니다. 자연스럽고 깔끔한 메이크업이 핵심이며, 누구나 쉽게 따라할 수 있습니다.",
                source="youtube_beauty",
                url="https://example.com/kbeauty-tutorial",
                date=datetime.now(),
                author="뷰티 유튜버"
            ),
            ScrapedPost(
                title="한국 스킨케어 루틴 공유",
                content="10단계 한국 스킨케어 루틴을 공유합니다. 각 단계별로 사용하는 제품과 방법을 자세히 설명했으며, 피부 개선 효과를 경험할 수 있습니다.",
                source="naver_beauty",
                url="https://example.com/korean-skincare-routine",
                date=datetime.now(),
                author="스킨케어 전문가"
            ),
            ScrapedPost(
                title="K뷰티 신상품 출시 정보",
                content="이번 달 새로 출시되는 K뷰티 브랜드들의 신상품 정보를 모아보았습니다. 특히 마스크팩과 에센스 제품들이 주목받고 있습니다.",
                source="naver_beauty",
                url="https://example.com/kbeauty-new-products",
                date=datetime.now(),
                author="뷰티 리뷰어"
            )
        ]
        
        logger.info(f"Generated {len(mock_posts)} mock posts for testing")
        return mock_posts

async def main():
    """Main function to run the scraper."""
    scraper = KBeautyScraper()
    posts = await scraper.scrape_all_sources()
    
    # Save to output directory
    output_file = config.output.output_dir / f"scraped_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    scraper.save_scraped_data(posts, output_file)
    
    return posts

if __name__ == "__main__":
    asyncio.run(main()) 