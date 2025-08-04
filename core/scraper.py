"""
Modular scraper for K-Beauty content collection (Serverless-compatible version)
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import os

from bs4 import BeautifulSoup
import aiohttp
import requests

from core.config import config
from core.models import ScrapedPost

logger = logging.getLogger(__name__)

class KBeautyScraper:
    """Modular scraper for K-beauty content (serverless-compatible)."""
    
    def __init__(self):
        self.config = config.scraping
        self.sources_config = config.get_sources_config()
        self.scraped_posts: List[ScrapedPost] = []
        
    async def scrape_all_sources(self) -> List[ScrapedPost]:
        """Scrape content from all configured sources."""
        logger.info("Starting K-beauty content scraping (serverless mode)...")
        
        # In serverless environment, use mock data or simple HTTP requests
        if os.getenv("VERCEL") or os.getenv("TEST_MODE", "false").lower() == "true":
            logger.info("Running in serverless/test mode with mock data")
            return self._generate_mock_data()
        
        # For local development, try simple HTTP scraping
        try:
            # Simple HTTP-based scraping (no browser automation)
            naver_posts = await self._scrape_naver_simple()
            instagram_posts = await self._scrape_instagram_simple()
            youtube_posts = await self._scrape_youtube_simple()
            
            # Combine all scraped data
            self.scraped_posts = naver_posts + instagram_posts + youtube_posts
            
            # Filter for relevance
            relevant_posts = self._filter_relevant_content()
            
            logger.info(f"Successfully scraped {len(relevant_posts)} relevant posts")
            return relevant_posts
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            logger.info("Falling back to mock data")
            return self._generate_mock_data()
    
    async def _scrape_naver_simple(self) -> List[ScrapedPost]:
        """Simple HTTP-based Naver scraping."""
        logger.info("Scraping Naver Beauty content (simple mode)...")
        scraped_posts = []
        
        naver_config = self.sources_config["naver_beauty"]
        
        async with aiohttp.ClientSession() as session:
            for url in naver_config["urls"]:
                try:
                    headers = {"User-Agent": self.config.user_agent}
                    async with session.get(url, headers=headers, timeout=10) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Extract basic content (simplified)
                            posts = soup.find_all('li', class_='bx')
                            
                            for post in posts[:self.config.max_posts_per_source]:
                                try:
                                    post_data = self._extract_post_data_simple(post)
                                    if post_data:
                                        scraped_posts.append(post_data)
                                except Exception as e:
                                    logger.warning(f"Error extracting post data: {e}")
                                    continue
                                    
                except Exception as e:
                    logger.warning(f"Error scraping {url}: {e}")
                    continue
                    
        return scraped_posts
    
    async def _scrape_instagram_simple(self) -> List[ScrapedPost]:
        """Simple Instagram scraping (limited in serverless)."""
        logger.info("Scraping Instagram content (simple mode)...")
        # Instagram requires authentication and has anti-bot measures
        # For serverless, we'll return mock data
        return []
    
    async def _scrape_youtube_simple(self) -> List[ScrapedPost]:
        """Simple YouTube scraping (limited in serverless)."""
        logger.info("Scraping YouTube content (simple mode)...")
        # YouTube has complex anti-bot measures
        # For serverless, we'll return mock data
        return []
    
    def _extract_post_data_simple(self, post_element) -> Optional[ScrapedPost]:
        """Extract post data using BeautifulSoup (simplified)."""
        try:
            # Extract title
            title_elem = post_element.find('a', class_='title_link')
            title = title_elem.get_text(strip=True) if title_elem else "K-Beauty Trend Post"
            
            # Extract content
            content_elem = post_element.find('div', class_='dsc')
            content = content_elem.get_text(strip=True) if content_elem else "Korean beauty trend content"
            
            # Extract date
            date_elem = post_element.find('span', class_='date')
            date_str = date_elem.get_text(strip=True) if date_elem else datetime.now().isoformat()
            
            # Extract author
            author_elem = post_element.find('span', class_='author')
            author = author_elem.get_text(strip=True) if author_elem else "K-Beauty Community"
            
            return ScrapedPost(
                id=f"post_{datetime.now().timestamp()}",
                title=title,
                content=content,
                author=author,
                source="naver_beauty",
                url="https://search.naver.com",
                published_date=date_str,
                relevance_score=0.8
            )
            
        except Exception as e:
            logger.warning(f"Error extracting post data: {e}")
            return None
    
    def _filter_relevant_content(self) -> List[ScrapedPost]:
        """Filter content for relevance to K-beauty."""
        relevant_posts = []
        
        kbeauty_keywords = [
            "k-beauty", "korean beauty", "korean skincare", "korean makeup",
            "korean cosmetics", "korean skin", "korean routine", "korean products",
            "k뷰티", "한국화장품", "한국스킨케어", "한국메이크업"
        ]
        
        for post in self.scraped_posts:
            content_lower = (post.title + " " + post.content).lower()
            
            # Check for K-beauty keywords
            relevance_score = 0
            for keyword in kbeauty_keywords:
                if keyword.lower() in content_lower:
                    relevance_score += 0.3
            
            # Update relevance score
            post.relevance_score = min(relevance_score, 1.0)
            
            # Include posts with some relevance
            if post.relevance_score > 0.1:
                relevant_posts.append(post)
        
        return relevant_posts
    
    def save_scraped_data(self, posts: List[ScrapedPost], output_file: Path):
        """Save scraped data to file."""
        try:
            output_file.parent.mkdir(exist_ok=True)
            
            data = {
                "scraped_at": datetime.now().isoformat(),
                "total_posts": len(posts),
                "posts": [post.to_dict() for post in posts]
            }
            
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Scraped data saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving scraped data: {e}")
    
    def _generate_mock_data(self) -> List[ScrapedPost]:
        """Generate mock data for testing and serverless environments."""
        logger.info("Generating mock K-beauty trend data...")
        
        mock_posts = [
            ScrapedPost(
                id="mock_1",
                title="Glass Skin Trend Continues to Dominate K-Beauty",
                content="The glass skin trend shows no signs of slowing down. Korean beauty enthusiasts are focusing on achieving that perfect, dewy complexion through multi-step routines and innovative products.",
                author="K-Beauty Expert",
                source="naver_beauty",
                url="https://example.com/glass-skin",
                published_date=datetime.now().isoformat(),
                relevance_score=0.95
            ),
            ScrapedPost(
                id="mock_2",
                title="Cushion Foundation Innovation: New Formulas for 2024",
                content="Korean cushion foundations are evolving with new formulas that provide better coverage, longer wear, and skincare benefits. Brands are incorporating ingredients like hyaluronic acid and niacinamide.",
                author="Beauty Trend Analyst",
                source="instagram_beauty",
                url="https://example.com/cushion-foundation",
                published_date=datetime.now().isoformat(),
                relevance_score=0.88
            ),
            ScrapedPost(
                id="mock_3",
                title="Propolis and Honey Extracts: The New Star Ingredients",
                content="Propolis and honey extracts are becoming increasingly popular in Korean skincare. These natural ingredients offer antibacterial, anti-inflammatory, and moisturizing properties.",
                author="Skincare Researcher",
                source="youtube_beauty",
                url="https://example.com/propolis-honey",
                published_date=datetime.now().isoformat(),
                relevance_score=0.82
            ),
            ScrapedPost(
                id="mock_4",
                title="K-Beauty Minimalism: Less is More Approach",
                content="Korean beauty is embracing minimalism with streamlined routines and multi-functional products. Consumers are focusing on quality over quantity in their skincare collections.",
                author="Beauty Minimalist",
                source="naver_beauty",
                url="https://example.com/k-beauty-minimalism",
                published_date=datetime.now().isoformat(),
                relevance_score=0.78
            ),
            ScrapedPost(
                id="mock_5",
                title="Sustainable K-Beauty: Eco-Friendly Packaging and Ingredients",
                content="Sustainability is becoming a major focus in Korean beauty. Brands are introducing refillable packaging, biodegradable materials, and clean ingredient formulations.",
                author="Eco Beauty Advocate",
                source="instagram_beauty",
                url="https://example.com/sustainable-k-beauty",
                published_date=datetime.now().isoformat(),
                relevance_score=0.75
            )
        ]
        
        logger.info(f"Generated {len(mock_posts)} mock posts")
        return mock_posts

async def main():
    """Main function for testing."""
    scraper = KBeautyScraper()
    posts = await scraper.scrape_all_sources()
    print(f"Scraped {len(posts)} posts")
    
    # Save to file
    output_file = Path("data/scraped_posts.json")
    scraper.save_scraped_data(posts, output_file)

if __name__ == "__main__":
    asyncio.run(main()) 