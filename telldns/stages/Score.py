"""
ScoreStage - Rank subdomains by importance
"""

from .base import BaseStage
from ..utils.logger import get_logger


class ScoreStage(BaseStage):
    """Rank subdomains based on various factors"""
    
    def __init__(self):
        self.logger = get_logger()
    
    async def run(self, context):
        """Score and rank subdomains"""
        discovered = context.discovered
        validated = context.validated
        
        self.logger.info(f"Scoring {len(discovered)} subdomains")
        
        scores = {}
        
        for subdomain in discovered:
            score = 50  # Base score
            
            # Factor 1: Has IP (DNS resolved)
            if subdomain in validated:
                score += 20
            
            # Factor 2: Length (shorter is better)
            if len(subdomain) < 5:
                score += 10
            elif len(subdomain) > 20:
                score -= 10
            
            # Factor 3: Keywords (high value subdomains)
            high_value = ['admin', 'api', 'vpn', 'mail', 'portal', 'dashboard', 'cpanel', 'whm']
            for keyword in high_value:
                if keyword in subdomain.lower():
                    score += 15
                    break
            
            # Factor 4: Contains digits (less interesting usually)
            if any(c.isdigit() for c in subdomain):
                score -= 5
            
            # Factor 5: Source
            source = context.metadata.get(subdomain, {}).get('source', 'unknown')
            if source == 'active':
                score += 5
            elif source == 'generated':
                score -= 10
            
            scores[subdomain] = max(0, min(100, score))
        
        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Store in context
        context.metadata['scores'] = scores
        context.metadata['ranked'] = [sub for sub, _ in ranked]
        
        self.logger.info(f"Top 5 subdomains:")
        for i, (sub, score) in enumerate(ranked[:5], 1):
            self.logger.info(f"  {i}. {sub}.{context.domain} (score: {score})")
        
        return scores
