"""
AlienVault OTX (Open Threat Exchange) source
"""

import aiohttp
from typing import Set


async def fetch_alienvault(domain: str) -> Set[str]:
    """Fetch subdomains from AlienVault OTX"""
    subdomains = set()
    
    try:
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    
                    for item in data.get('passive_dns', []):
                        hostname = item.get('hostname', '')
                        if hostname and hostname.endswith(f".{domain}"):
                            sub = hostname.replace(f".{domain}", "")
                            if '*' not in sub:
                                subdomains.add(sub)
    except Exception:
        pass
    
    return subdomains
