"""
DNSResolver - Async DNS resolver with rotation and stealth
"""

import asyncio
import random
import dns.resolver
import dns.asyncresolver
from typing import List, Optional


# DNS resolvers list (public, reliable)
RESOLVERS = [
    '8.8.8.8',      # Google
    '8.8.4.4',      # Google
    '1.1.1.1',      # Cloudflare
    '1.0.0.1',      # Cloudflare
    '9.9.9.9',      # Quad9
    '208.67.222.222', # OpenDNS
    '208.67.220.220', # OpenDNS
    '94.140.14.14',   # AdGuard
    '94.140.15.15',   # AdGuard
    '76.76.19.19',    # Alternate DNS
]


class DNSResolver:
    """Async DNS resolver with resolver rotation and stealth delays"""
    
    def __init__(self, timeout: float = 3.0, stealth: bool = False, max_concurrent: int = 500):
        self.timeout = timeout
        self.stealth = stealth
        self.max_concurrent = max_concurrent
        self.resolver_index = 0
        self._resolver = None
    
    def _get_resolver(self):
        """Get or create async resolver with current nameserver"""
        resolver = dns.asyncresolver.Resolver()
        resolver.nameservers = [RESOLVERS[self.resolver_index % len(RESOLVERS)]]
        resolver.timeout = self.timeout
        resolver.lifetime = self.timeout * 2
        return resolver
    
    def _rotate_resolver(self):
        """Rotate to next DNS resolver"""
        self.resolver_index = (self.resolver_index + 1) % len(RESOLVERS)
    
    async def resolve(self, domain: str, retry: int = 1) -> Optional[List[str]]:
        """Resolve domain to IP addresses"""
        # Add stealth delay if enabled
        if self.stealth:
            await asyncio.sleep(random.uniform(0.01, 0.05))
        
        # Rotate resolver every 50 requests
        if random.randint(1, 50) == 1:
            self._rotate_resolver()
        
        resolver = self._get_resolver()
        
        try:
            answers = await resolver.resolve(domain, 'A')
            return [str(answer) for answer in answers]
        
        except dns.resolver.NXDOMAIN:
            return None
        except dns.resolver.NoAnswer:
            return None
        except dns.resolver.Timeout:
            if retry > 0:
                await asyncio.sleep(0.5)
                return await self.resolve(domain, retry - 1)
            return None
        except Exception:
            return None
