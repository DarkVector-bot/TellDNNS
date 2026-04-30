"""
ActiveStage - Bruteforce subdomains using wordlist
"""

import asyncio
from typing import List

from .base import BaseStage
from ..network.resolver import DNSResolver
from ..utils.logger import get_logger


class ActiveStage(BaseStage):
    """Active bruteforce with wordlist"""
    
    def __init__(self):
        self.logger = get_logger()
        self.resolver = None
    
    async def run(self, context):
        """Run active bruteforce"""
        domain = context.domain
        wordlist = context.wordlist
        concurrency = context.config.get('concurrency', 500)
        stealth = context.config.get('stealth', False)
        timeout = context.config.get('timeout', 3.0)
        
        self.logger.info(f"Starting active bruteforce with {len(wordlist)} words")
        
        # Initialize resolver
        self.resolver = DNSResolver(
            timeout=timeout,
            stealth=stealth,
            max_concurrent=concurrency
        )
        
        # Filter already found
        already_found = context.discovered
        to_check = [w for w in wordlist if w not in already_found]
        
        self.logger.info(f"Checking {len(to_check)} new subdomains")
        
        # Run bruteforce
        semaphore = asyncio.Semaphore(concurrency)
        
        async def check(subdomain: str):
            async with semaphore:
                full = f"{subdomain}.{domain}"
                result = await self.resolver.resolve(full)
                context.add_query_result(result is not None)
                return subdomain, result
        
        tasks = [check(word) for word in to_check]
        found_count = 0
        
        for coro in asyncio.as_completed(tasks):
            subdomain, ips = await coro
            if ips:
                found_count += 1
                context.add_discovered(subdomain, 'active', ips)
                
                if found_count % 10 == 0:
                    self.logger.info(f"Active progress: found {found_count} so far")
        
        self.logger.info(f"Active stage completed: found {found_count} new subdomains")
        
        return context.discovered
