"""
Certificate Transparency Logs (crt.sh) source
"""

import aiohttp
from typing import Set


async def fetch_crtsh(domain: str) -> Set[str]:
    """Fetch subdomains from crt.sh"""
    subdomains = set()
    
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    
                    for entry in data:
                        name = entry.get('name_value', '')
                        if name:
                            # Split multiple names (sometimes separated by newline)
                            for part in name.split('\n'):
                                part = part.strip().lower()
                                # Extract subdomain
                                if part.endswith(f".{domain}") and part != domain:
                                    sub = part.replace(f".{domain}", "")
                                    # Remove wildcards
                                    if '*' not in sub and len(sub) > 0:
                                        subdomains.add(sub)
    except Exception:
        pass
    
    return subdomains
