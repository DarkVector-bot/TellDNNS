"""
GenerateStage - Generate new subdomains using AI and permutations
"""

import asyncio
from typing import Set, List

from .base import BaseStage
from ..intelligence.predictor import AIPredictor
from ..utils.logger import get_logger


class GenerateStage(BaseStage):
    """Generate new subdomains from existing ones"""
    
    def __init__(self):
        self.logger = get_logger()
        self.ai_predictor = None
    
    async def run(self, context):
        """Generate new subdomains"""
        use_ai = context.config.get('use_ai', True)
        use_permutation = context.config.get('use_permutation', True)
        
        existing = context.discovered
        if not existing:
            self.logger.info("No existing subdomains to generate from")
            return set()
        
        generated = set()
        
        # Permutation attack
        if use_permutation:
            perm_result = await self._permutation_attack(existing)
            generated.update(perm_result)
            self.logger.info(f"Permutation generated {len(perm_result)} candidates")
        
        # AI prediction
        if use_ai:
            ai_result = await self._ai_prediction(existing, context.domain)
            generated.update(ai_result)
            self.logger.info(f"AI predicted {len(ai_result)} candidates")
        
        # Filter and add to context
        already_found = context.discovered
        new_candidates = generated - already_found
        
        # Quick validate candidates
        validated = await self._quick_validate(list(new_candidates)[:500], context)
        
        for subdomain in validated:
            context.add_discovered(subdomain, 'generated')
        
        self.logger.info(f"Generate stage completed: found {len(validated)} new subdomains")
        
        return validated
    
    async def _permutation_attack(self, existing: Set[str]) -> Set[str]:
        """Generate permutations from existing subdomains"""
        permutations = set()
        
        prefixes = ['dev', 'staging', 'test', 'old', 'new', 'backup', 'api', 'admin']
        suffixes = ['-dev', '-staging', '-test', '-old', '-new', '-backup', '-api', '-v1', '-v2']
        numbers = ['1', '2', '3', '01', '02', '03']
        
        for sub in existing:
            # Add prefixes
            for p in prefixes:
                permutations.add(f"{p}-{sub}")
                permutations.add(f"{p}{sub}")
            
            # Add suffixes
            for s in suffixes:
                permutations.add(f"{sub}{s}")
            
            # Add numbers
            for n in numbers:
                permutations.add(f"{sub}{n}")
                permutations.add(f"{n}{sub}")
            
            # Handle hyphenated
            if '-' in sub:
                parts = sub.split('-')
                if len(parts) >= 2:
                    permutations.add(f"{parts[0]}{parts[1]}")
                    permutations.add(f"{parts[1]}-{parts[0]}")
        
        return permutations
    
    async def _ai_prediction(self, existing: Set[str], domain: str) -> Set[str]:
        """Use AI to predict new subdomains"""
        if not self.ai_predictor:
            self.ai_predictor = AIPredictor()
        
        try:
            predictions = await self.ai_predictor.predict(existing, domain)
            return set(predictions[:100])
        except Exception as e:
            self.logger.debug(f"AI prediction failed: {e}")
            return set()
    
    async def _quick_validate(self, candidates: List[str], context) -> List[str]:
        """Quick DNS validation for generated candidates"""
        from ..network.resolver import DNSResolver
        
        resolver = DNSResolver(timeout=2.0, stealth=True)
        domain = context.domain
        concurrency = 100
        
        semaphore = asyncio.Semaphore(concurrency)
        validated = []
        
        async def check(subdomain: str):
            async with semaphore:
                full = f"{subdomain}.{domain}"
                result = await resolver.resolve(full)
                return subdomain if result else None
        
        tasks = [check(sub) for sub in candidates[:500]]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            if result:
                validated.append(result)
        
        return validated
