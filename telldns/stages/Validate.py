"""
ValidateStage - Validate discovered subdomains with DNS + HTTP check
"""

import asyncio
from typing import Dict

from .base import BaseStage
from ..network.resolver import DNSResolver
from ..utils.logger import get_logger


class ValidateStage(BaseStage):
    """Validate subdomains with DNS resolution"""
    
    def __init__(self):
        self.logger = get_logger()
        self.resolver = None
    
    async def run(self, context):
        """Validate all discovered subdomains"""
        discovered = context.discovered
        domain = context.domain
        timeout = context.config.get('timeout', 3.0)
        stealth = context.config.get('stealth', False)
        
        self.logger.info(f"Validating {len(discovered)} subdomains")
        
        # Initialize resolver
        self.resolver = DNSResolver(timeout=timeout, stealth=stealth)
        
        # Validate each subdomain
        semaphore = asyncio.Semaphore(100)
        validated = {}
        
        async def validate(subdomain: str):
            async with semaphore:
                full = f"{subdomain}.{domain}"
                ips = await self.resolver.resolve(full)
                return subdomain, ips
        
        tasks = [validate(sub) for sub in discovered]
        
        completed = 0
        for coro in asyncio.as_completed(tasks):
            sub, ips = await coro
            completed += 1
            if ips:
                validated[sub] = ips
            if completed % 50 == 0:
                self.logger.info(f"Validation progress: {completed}/{len(discovered)}")
        
        # Update context with validated IPs
        for subdomain, ips in validated.items():
            context.validated[subdomain] = ips
        
        self.logger.info(f"Validation completed: {len(validated)} subdomains resolved")
        
        return validated
