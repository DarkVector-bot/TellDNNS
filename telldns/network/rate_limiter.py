"""
RateLimiter - Smart rate limiting for DNS queries
"""

import asyncio
import time
from collections import deque
from typing import Optional


class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, rate: int = 100, per_second: float = 1.0):
        """
        Args:
            rate: Number of requests allowed
            per_second: Time window in seconds
        """
        self.rate = rate
        self.per_second = per_second
        self.tokens = rate
        self.updated_at = time.monotonic()
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> bool:
        """Acquire a token, returns True if available"""
        async with self._lock:
            now = time.monotonic()
            time_passed = now - self.updated_at
            self.tokens = min(self.rate, self.tokens + time_passed * (self.rate / self.per_second))
            self.updated_at = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            
            # Wait for next token
            wait_time = (1 - self.tokens) / (self.rate / self.per_second)
            await asyncio.sleep(wait_time)
            self.tokens = 0
            self.updated_at = time.monotonic()
            return True
    
    async def __aenter__(self):
        await self.acquire()
        return self
    
    async def __aexit__(self, *args):
        pass


class AdaptiveRateLimiter:
    """Rate limiter that adapts based on success/failure rate"""
    
    def __init__(self, initial_rate: int = 500, min_rate: int = 50, max_rate: int = 1000):
        self.current_rate = initial_rate
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.success_count = 0
        self.failure_count = 0
        self.window_size = 100
        self._rate_limiter = RateLimiter(initial_rate, 1.0)
    
    async def acquire(self):
        """Acquire with adaptive rate limiting"""
        await self._rate_limiter.acquire()
    
    def record_success(self):
        """Record successful request"""
        self.success_count += 1
        self._adjust_rate()
    
    def record_failure(self):
        """Record failed request"""
        self.failure_count += 1
        self._adjust_rate()
    
    def _adjust_rate(self):
        """Adjust rate based on recent success rate"""
        total = self.success_count + self.failure_count
        if total >= self.window_size:
            success_rate = self.success_count / total
            
            if success_rate > 0.9 and self.current_rate < self.max_rate:
                # Increase rate
                self.current_rate = min(self.max_rate, int(self.current_rate * 1.1))
            elif success_rate < 0.5 and self.current_rate > self.min_rate:
                # Decrease rate
                self.current_rate = max(self.min_rate, int(self.current_rate * 0.8))
            
            # Reset counters
            self.success_count = 0
            self.failure_count = 0
            
            # Update rate limiter
            self._rate_limiter = RateLimiter(self.current_rate, 1.0)
