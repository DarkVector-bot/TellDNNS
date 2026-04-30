"""
DNSDumpster source
"""

import aiohttp
from typing import Set


async def fetch_dnsdumpster(domain: str) -> Set[str]:
    """Fetch subdomains from DNSDumpster"""
    subdomains = set()
    
    try:
        # DNSDumpster API endpoint
        url = f"https://dnsdumpster.com/api/subdomains/{domain}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    
                    if isinstance(data, list):
                        for item in data:
                            hostname = item.get('host', '')
                            if hostname and hostname.endswith(f".{domain}"):
                                sub = hostname.replace(f".{domain}", "")
                                if '*' not in sub:
                                    subdomains.add(sub)
    except Exception:
        pass
    
    return subdomains
