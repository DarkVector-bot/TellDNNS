"""
PassiveStage - Collect subdomains from public sources
"""

import asyncio
from typing import Set

from .base import BaseStage
from ..sources import (
    fetch_crtsh,
    fetch_alienvault,
    fetch_rapiddns,
    fetch_wayback,
    fetch_dnsdumpster
)
from ..utils.logger import get_logger


class PassiveStage(BaseStage):
    """Passive enumeration from multiple sources"""
    
    def __init__(self):
        self.logger = get_logger()
        self.sources = [
            ('crtsh', fetch_crtsh),
            ('alienvault', fetch_alienvault),
            ('rapiddns', fetch_rapiddns),
            ('wayback', fetch_wayback),
            ('dnsdumpster', fetch_dnsdumpster),
        ]
    
    async def run(self, context):
        """Run passive enumeration"""
        domain = context.domain
        all_found = set()
        
        self.logger.info(f"Starting passive enumeration for {domain}")
        
        # Run all sources concurrently
        tasks = []
        for source_name, source_func in self.sources:
            tasks.append(self._fetch_source(source_name, source_func, domain))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collect results
        for result in results:
            if isinstance(result, Exception):
                self.logger.debug(f"Source error: {result}")
                continue
            if result:
                all_found.update(result)
        
        # Add to context
        for subdomain in all_found:
            context.add_discovered(subdomain, 'passive')
        
        self.logger.info(f"Passive stage completed: found {len(all_found)} subdomains")
        
        return all_found
    
    async def _fetch_source(self, name: str, func, domain: str) -> Set[str]:
        """Fetch from a single source with error handling"""
        try:
            self.logger.debug(f"Querying {name}...")
            result = await func(domain)
            self.logger.debug(f"{name} returned {len(result)} results")
            return result
        except Exception as e:
            self.logger.debug(f"{name} failed: {e}")
            return set()
