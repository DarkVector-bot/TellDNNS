"""
Wayback Machine (archive.org) source
"""

import aiohttp
from typing import Set


async def fetch_wayback(domain: str) -> Set[str]:
    """Fetch subdomains from Wayback Machine"""
    subdomains = set()
    
    try:
        url = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&collapse=urlkey"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    
                    # First row is headers
                    for row in data[1:]:
                        if len(row) > 0:
                            url_text = row[0]
                            # Extract subdomain from URL
                            if domain in url_text:
                                # Try to extract subdomain
                                parts = url_text.split('.')
                                if len(parts) >= 3:
                                    # Ambil bagian pertama sebagai subdomain
                                    potential_sub = parts[0]
                                    if potential_sub and '*' not in potential_sub and len(potential_sub) > 0:
                                        # Validasi tidak mengandung protocol
                                        if not potential_sub.startswith('http'):
                                            subdomains.add(potential_sub)
    except Exception:
        pass
    
    return subdomains
