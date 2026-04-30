"""
Config - Configuration loader for TellDNS
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, asdict


DEFAULT_CONFIG = {
    'concurrency': 500,
    'timeout': 3.0,
    'stealth': False,
    'resolvers': [
        '8.8.8.8',
        '1.1.1.1',
        '9.9.9.9',
        '208.67.222.222'
    ],
    'passive_sources': {
        'crtsh': True,
        'alienvault': True,
        'rapiddns': True,
        'wayback': True,
        'dnsdumpster': True
    },
    'output': {
        'format': 'txt',
        'verbose': False
    }
}


@dataclass
class TellDNSConfig:
    """Configuration class for TellDNS"""
    concurrency: int = 500
    timeout: float = 3.0
    stealth: bool = False
    resolvers: list = None
    passive_sources: dict = None
    output: dict = None
    
    def __post_init__(self):
        if self.resolvers is None:
            self.resolvers = DEFAULT_CONFIG['resolvers']
        if self.passive_sources is None:
            self.passive_sources = DEFAULT_CONFIG['passive_sources']
        if self.output is None:
            self.output = DEFAULT_CONFIG['output']
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TellDNSConfig':
        """Create config from dictionary"""
        return cls(**data)


def load_config(config_path: str = None) -> TellDNSConfig:
    """Load configuration from file"""
    config = TellDNSConfig()
    
    # Try to load from default paths
    paths = [
        config_path,
        'config/default.yaml',
        'config/default.yml',
        'config.json',
        str(Path.home() / '.telldns' / 'config.yaml'),
        str(Path.home() / '.telldns' / 'config.json')
    ]
    
    for path in paths:
        if path and os.path.exists(path):
            try:
                if path.endswith(('.yaml', '.yml')):
                    with open(path, 'r') as f:
                        data = yaml.safe_load(f)
                        config = TellDNSConfig.from_dict(data)
                elif path.endswith('.json'):
                    with open(path, 'r') as f:
                        data = json.load(f)
                        config = TellDNSConfig.from_dict(data)
                break
            except Exception:
                pass
    
    return config


def save_config(config: TellDNSConfig, config_path: str):
    """Save configuration to file"""
    # Create directory if needed
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)
    
    if config_path.endswith(('.yaml', '.yml')):
        with open(config_path, 'w') as f:
            yaml.dump(config.to_dict(), f)
    elif config_path.endswith('.json'):
        with open(config_path, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)
