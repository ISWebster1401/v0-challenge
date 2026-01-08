"""
Cache management utilities
"""
from datetime import datetime
from typing import Dict, Optional
from collections import defaultdict
import os


# Global cache with date-based keys
cache: Dict[str, Dict] = defaultdict(lambda: {
    "articles": [],
    "timestamp": None,
    "ttl": int(os.getenv("CACHE_TTL", 900))  # 15 minutes default
})

# Full summary cache (by URL) - 24 hour TTL
full_summary_cache: Dict[str, Dict] = {}


def get_cache_key_str(from_date: Optional[str] = None, to_date: Optional[str] = None, topic: Optional[str] = None) -> str:
    """Generate cache key based on date range and topic (using string dates)"""
    date_part = ""
    if from_date and to_date:
        date_part = f"{from_date}_{to_date}"
    elif from_date:
        date_part = f"{from_date}_"
    elif to_date:
        date_part = f"_{to_date}"
    else:
        date_part = "default"
    
    if topic:
        return f"{date_part}_topic_{topic.lower()}"
    return date_part


def is_cache_valid(cache_key: str) -> bool:
    """Check if cache is still valid for given key"""
    cache_entry = cache[cache_key]
    if not cache_entry["timestamp"] or not cache_entry["articles"]:
        return False
    
    age = (datetime.now() - cache_entry["timestamp"]).total_seconds()
    return age < cache_entry["ttl"]


def get_cache_age(cache_key: str) -> Optional[int]:
    """Get cache age in seconds for given key"""
    cache_entry = cache[cache_key]
    if not cache_entry["timestamp"]:
        return None
    return int((datetime.now() - cache_entry["timestamp"]).total_seconds())
