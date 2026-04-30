"""
RapidDNS.io source
"""

import aiohttp
import re
from typing import Set


async def fetch_rapiddns(domain: str) -> Set[str]:
    """Fetch subdomains from RapidDNS"""
    subdomains = set()
    
    try:
        url = f"https://rapiddns.io/subdomain/{domain}?full=1"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    
                    # Simple extraction (RapidDNS returns HTML)
                    pattern = r'([a-zA-Z0-9][a-zA-Z0-9\-_]+(?:\.[a-zA-Z0-9\-_]+)*)\.' + re.escape(domain)
                    matches = re.findall(pattern, html)
                    
                    for match in matches:
                        if match and '*' not in match:
                            subdomains.add(match)
    except Exception:
        pass
    
    return subdomains
