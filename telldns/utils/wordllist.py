"""
Wordlist - Wordlist loader and manager for TellDNS
"""

import os
import gzip
from pathlib import Path
from typing import List, Optional


# Default wordlist (common subdomains)
DEFAULT_WORDS = [
    'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
    'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'ns',
    'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3',
    'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx',
    'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar',
    'wiki', 'web', 'media', 'email', 'images', 'img', 'download', 'dns',
    'stats', 'dashboard', 'portal', 'manage', 'start', 'info', 'apps', 'video',
    'sip', 'dns2', 'api', 'cdn', 'remote', 'server', 'vps', 'help', 'go',
    'share', 'upload', 'auth', 'login', 'signin', 'signup', 'register', 'pay',
    'billing', 'account', 'user', 'customer', 'store', 'checkout', 'crm', 'erp',
    'hr', 'intranet', 'extranet', 'office', 'exchange', 'backup', 'storage',
    'db', 'database', 'redis', 'jenkins', 'gitlab', 'docker', 'kubernetes',
    'staging', 'production', 'prod', 'development', 'sandbox', 'qa', 'uat',
    'preprod', 'loadtest', 'analytics', 'monitoring', 'logs', 'metrics',
    'grafana', 'prometheus', 'kibana', 'elastic', 'kafka', 'rabbitmq'
]


def load_wordlist(wordlist_path: Optional[str] = None) -> List[str]:
    """Load wordlist from file or return default"""
    
    # Try to load from provided path
    if wordlist_path and os.path.exists(wordlist_path):
        return _load_from_file(wordlist_path)
    
    # Try default paths
    default_paths = [
        'wordlists/default.txt',
        'wordlists/common.txt',
        'telldns/wordlists/default.txt',
        str(Path.home() / '.telldns' / 'wordlist.txt')
    ]
    
    for path in default_paths:
        if os.path.exists(path):
            return _load_from_file(path)
    
    # Return default wordlist
    return DEFAULT_WORDS.copy()


def _load_from_file(filepath: str) -> List[str]:
    """Load wordlist from text file (supports .txt and .txt.gz)"""
    words = []
    
    try:
        if filepath.endswith('.gz'):
            with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    if word and not word.startswith('#'):
                        words.append(word)
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    if word and not word.startswith('#'):
                        words.append(word)
    except Exception:
        return DEFAULT_WORDS.copy()
    
    return words if words else DEFAULT_WORDS.copy()


def save_wordlist(words: List[str], filepath: str):
    """Save wordlist to file"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for word in sorted(set(words)):
            f.write(f"{word}\n")


def merge_wordlists(*wordlists: List[str]) -> List[str]:
    """Merge multiple wordlists and remove duplicates"""
    merged = set()
    for wl in wordlists:
        merged.update(wl)
    return sorted(merged)
