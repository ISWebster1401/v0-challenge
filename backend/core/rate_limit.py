"""
Rate limiting utilities
"""
from datetime import datetime
from collections import deque

# Rate limiting for full summaries (10 per minute)
rate_limit_requests = deque()
RATE_LIMIT_COUNT = 10
RATE_LIMIT_WINDOW = 60  # seconds


def check_rate_limit() -> bool:
    """Check if rate limit allows new request"""
    now = datetime.now()
    
    # Remove requests older than the rate limit window
    while rate_limit_requests and (now - rate_limit_requests[0]).total_seconds() > RATE_LIMIT_WINDOW:
        rate_limit_requests.popleft()
    
    # Check if we're at the limit
    if len(rate_limit_requests) >= RATE_LIMIT_COUNT:
        return False
    
    # Add current request
    rate_limit_requests.append(now)
    return True
