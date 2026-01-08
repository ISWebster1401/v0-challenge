from openai import OpenAI
from typing import List, Dict
import asyncio
import json
import re

class AIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def summarize_article(self, title: str, description: str) -> str:
        """
        Generate a concise 2-3 sentence summary of a news article
        
        Args:
            title: Article title
            description: Article description/excerpt
            
        Returns:
            AI-generated summary string
        """
        prompt = f"""Summarize the following tech news article in 2-3 clear, concise sentences. 
Focus on the key information and impact.

Title: {title}
Description: {description}

Summary:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a tech news summarizer. Create concise, informative summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            # Fallback to description if AI fails
            return description[:200] + "..." if len(description) > 200 else description
    
    async def summarize_articles_batch(self, articles: List[Dict]) -> List[Dict]:
        """
        Summarize multiple articles in parallel
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Articles with added 'summary' field
        """
        async def summarize_one(article):
            # Run synchronous OpenAI call in thread pool
            loop = asyncio.get_event_loop()
            summary = await loop.run_in_executor(
                None, 
                self.summarize_article,
                article["title"],
                article["description"]
            )
            article["summary"] = summary
            return article
        
        # Process all articles in parallel
        tasks = [summarize_one(article) for article in articles]
        return await asyncio.gather(*tasks)
    
    def summarize_full_article(self, title: str, content: str) -> str:
        """
        Generate a comprehensive 5-7 sentence summary of a full article
        
        Args:
            title: Article title
            content: Full article text content
            
        Returns:
            AI-generated comprehensive summary string
        """
        prompt = f"""Provide a comprehensive 5-7 sentence summary of this tech news article, covering all key points, implications, and context.

Title: {title}

Article Content:
{content[:4000]}  # Limit to 4000 chars to stay within token limits

Comprehensive Summary:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a tech news analyst. Create comprehensive, detailed summaries that cover all important aspects of the article."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating full summary: {e}")
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    def extract_topics_from_titles(self, titles: List[str]) -> List[str]:
        """
        Extract 5-8 main topics from article titles using OpenAI
        
        Args:
            titles: List of article titles
            
        Returns:
            List of 5-8 unique topic names
        """
        if not titles:
            return []
        
        # Combine titles into a single string
        titles_text = "\n".join([f"- {title}" for title in titles[:50]])  # Limit to 50 titles to avoid token limits
        
        prompt = f"""Analyze these tech news titles and extract 5-8 main topics/themes. 
Return ONLY a JSON array of topics. Topics should be from this list: AI, Crypto, Hardware, Software, Startups, Gaming, Security, Mobile, Cloud, Web3, Robotics, Social Media, Space, Electric Vehicles, etc.

Example: ["AI", "Hardware", "Gaming"]

Here are the titles:
{titles_text}

Return ONLY the JSON array, nothing else:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a tech news analyst. Extract main topics from news titles. Return only a JSON array."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3  # Lower temperature for more consistent results
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON response (handle both array and string formats)
            # Try to extract JSON array from response
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if json_match:
                topics = json.loads(json_match.group())
            else:
                # Try parsing entire response as JSON
                topics = json.loads(response_text)
            
            # Ensure it's a list
            if isinstance(topics, str):
                topics = json.loads(topics)
            
            if not isinstance(topics, list):
                topics = []
            
            # Remove duplicates and limit to 8
            unique_topics = []
            seen = set()
            for topic in topics:
                topic_str = str(topic).strip()
                if topic_str and topic_str not in seen:
                    seen.add(topic_str)
                    unique_topics.append(topic_str)
            
            # Return 5-8 topics
            return unique_topics[:8] if len(unique_topics) >= 5 else unique_topics
            
        except Exception as e:
            print(f"Error extracting topics with OpenAI: {e}")
            print(f"Response was: {response_text if 'response_text' in locals() else 'N/A'}")
            # Fallback: return empty list (frontend can handle this)
            return []

