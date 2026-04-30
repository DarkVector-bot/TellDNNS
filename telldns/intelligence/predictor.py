"""
AIPredictor - AI-based subdomain prediction using pattern recognition
"""

import random
from typing import List, Set
from collections import Counter


class AIPredictor:
    """Simple AI predictor for subdomains based on patterns"""
    
    def __init__(self):
        self.common_prefixes = ['dev', 'staging', 'test', 'prod', 'api', 'admin', 'mail', 'web']
        self.common_suffixes = ['api', 'admin', 'backup', 'cdn', 'static', 'media', 'upload']
        self.patterns = []
    
    async def predict(self, existing: Set[str], domain: str) -> List[str]:
        """Predict new subdomains based on existing ones"""
        predictions = set()
        
        if not existing:
            return []
        
        # Learn patterns from existing subdomains
        self._learn_patterns(existing)
        
        # Generate predictions
        for sub in existing:
            # Length-based predictions
            if len(sub) < 10:
                predictions.add(f"{sub}2")
                predictions.add(f"{sub}-v2")
            
            # Common prefix/suffix predictions
            for prefix in self.common_prefixes:
                if not sub.startswith(prefix):
                    predictions.add(f"{prefix}-{sub}")
            
            for suffix in self.common_suffixes:
                if not sub.endswith(suffix):
                    predictions.add(f"{sub}-{suffix}")
            
            # Number variations
            for num in ['1', '2', '3', '01', '02']:
                predictions.add(f"{sub}{num}")
                predictions.add(f"{num}{sub}")
        
        # Filter out existing ones
        predictions = [p for p in predictions if p not in existing]
        
        # Limit predictions
        return list(predictions)[:200]
    
    def _learn_patterns(self, existing: Set[str]):
        """Learn patterns from existing subdomains"""
        # Get common lengths
        lengths = [len(s) for s in existing]
        avg_length = sum(lengths) / len(lengths) if lengths else 0
        
        # Get common characters
        all_chars = ''.join(existing)
        common_chars = Counter(all_chars).most_common(5)
        
        self.patterns = {
            'avg_length': avg_length,
            'common_chars': common_chars
        }
