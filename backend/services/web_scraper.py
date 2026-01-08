import httpx
from typing import Optional
import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

class WebScraper:
    """Simple web scraper for extracting article content"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    async def extract_article_content(self, url: str) -> Optional[str]:
        """
        Extract main article text from a URL
        
        Args:
            url: Article URL
            
        Returns:
            Extracted article text or None if extraction fails
        """
        if not BeautifulSoup:
            raise ImportError("beautifulsoup4 is required for web scraping")
        
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
                    script.decompose()
                
                # Try to find article content in common tags
                article_content = None
                
                # Try <article> tag first
                article_tag = soup.find('article')
                if article_tag:
                    article_content = article_tag.get_text()
                else:
                    # Try <main> tag
                    main_tag = soup.find('main')
                    if main_tag:
                        article_content = main_tag.get_text()
                    else:
                        # Try finding by common class names
                        for selector in ['article-content', 'post-content', 'entry-content', 'story-body']:
                            content_div = soup.find(class_=re.compile(selector, re.I))
                            if content_div:
                                article_content = content_div.get_text()
                                break
                    
                    # Fallback: get all <p> tags
                    if not article_content:
                        paragraphs = soup.find_all('p')
                        if paragraphs:
                            article_content = ' '.join([p.get_text() for p in paragraphs])
                
                if not article_content:
                    print(f"No article content found in HTML structure for {url}")
                    return None
                
                # Clean up text
                text = ' '.join(article_content.split())
                
                # Check if we got meaningful content (more than 100 chars)
                if len(text) < 100:
                    print(f"Extracted content too short ({len(text)} chars) for {url}")
                    return None
                
                # Limit content length (articles can be very long)
                if len(text) > 5000:
                    text = text[:5000] + "..."
                
                return text if text else None
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                print(f"Access denied (403) for {url} - likely paywall or bot protection")
            else:
                print(f"HTTP error scraping article from {url}: {e}")
            return None
        except Exception as e:
            print(f"Error scraping article from {url}: {e}")
            return None

