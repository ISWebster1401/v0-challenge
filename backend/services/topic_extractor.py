from typing import List, Dict
from collections import Counter
import re

class TopicExtractor:
    """Extract trending topics from article titles using keyword matching"""
    
    # Topic keywords mapping
    TOPIC_KEYWORDS = {
        'AI': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'neural network', 'deep learning', 'gpt', 'chatgpt', 'llm', 'openai', 'claude', 'gemini'],
        'Crypto': ['crypto', 'cryptocurrency', 'bitcoin', 'ethereum', 'blockchain', 'nft', 'web3', 'defi', 'btc', 'eth'],
        'Hardware': ['hardware', 'cpu', 'gpu', 'processor', 'chip', 'intel', 'amd', 'nvidia', 'qualcomm', 'apple silicon', 'm1', 'm2', 'm3'],
        'Software': ['software', 'app', 'application', 'os', 'operating system', 'windows', 'linux', 'macos', 'ios', 'android'],
        'Startup': ['startup', 'unicorn', 'ipo', 'funding', 'venture capital', 'vc', 'series a', 'series b', 'seed round'],
        'Gaming': ['gaming', 'game', 'playstation', 'xbox', 'nintendo', 'steam', 'esports', 'gamer', 'console'],
        'Security': ['security', 'cybersecurity', 'hack', 'breach', 'vulnerability', 'malware', 'ransomware', 'phishing'],
        'Cloud': ['cloud', 'aws', 'azure', 'gcp', 'google cloud', 'amazon web services', 'serverless', 'kubernetes'],
        'Mobile': ['mobile', 'smartphone', 'iphone', 'android phone', 'samsung', 'apple', 'ios', 'android'],
        'Social Media': ['twitter', 'facebook', 'instagram', 'tiktok', 'linkedin', 'social media', 'meta'],
        'Electric Vehicles': ['ev', 'electric vehicle', 'tesla', 'electric car', 'battery', 'charging'],
        'Space': ['space', 'nasa', 'spacex', 'rocket', 'satellite', 'mars', 'moon', 'astronaut']
    }
    
    def extract_topics(self, articles: List[Dict]) -> List[str]:
        """
        Extract trending topics from article titles and summaries
        
        Args:
            articles: List of article dictionaries with 'title' and 'summary' fields
            
        Returns:
            List of top 5-8 topic names sorted by frequency
        """
        if not articles:
            return []
        
        # Count topic occurrences
        topic_counts = Counter()
        
        for article in articles:
            title = article.get('title', '').lower()
            summary = article.get('summary', '').lower()
            description = article.get('description', '').lower()
            
            # Combine all text for better matching
            combined_text = f"{title} {summary} {description}"
            
            # Check each topic's keywords
            for topic, keywords in self.TOPIC_KEYWORDS.items():
                for keyword in keywords:
                    # Use word boundaries for better matching
                    pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                    if re.search(pattern, combined_text):
                        topic_counts[topic] += 1
                        break  # Only count once per article per topic
        
        # Get top topics (5-8 most common)
        top_topics = [topic for topic, count in topic_counts.most_common(8)]
        
        # Return at least top 5, but up to 8 if available
        return top_topics[:8] if len(top_topics) >= 5 else top_topics
    
    def get_topic_keywords(self, topic: str) -> List[str]:
        """Get keywords for a specific topic"""
        return self.TOPIC_KEYWORDS.get(topic, [])