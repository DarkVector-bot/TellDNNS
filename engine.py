"""
Engine - Main orchestrator for TellDNS
"""

import asyncio
import sys
from pathlib import Path

from .context import ScanContext
from .pipeline import Pipeline
from ..stages.passive import PassiveStage
from ..stages.active import ActiveStage
from ..stages.generate import GenerateStage
from ..stages.validate import ValidateStage
from ..stages.score import ScoreStage
from ..stages.output import OutputStage
from ..utils.logger import setup_logger, get_logger
from ..utils.wordlist import load_wordlist


class TellDNSEngine:
    """Main engine that orchestrates everything"""
    
    def __init__(
        self,
        domain: str,
        wordlist_file: str = None,
        output_file: str = None,
        output_format: str = "txt",
        concurrency: int = 500,
        timeout: float = 3.0,
        stealth: bool = False,
        use_ai: bool = True,
        use_permutation: bool = True,
        use_passive: bool = True,
        verbose: bool = False
    ):
        self.domain = domain
        self.output_file = output_file
        self.output_format = output_format
        self.verbose = verbose
        
        # Setup logger first
        setup_logger(verbose=verbose)
        self.logger = get_logger()
        
        # Load wordlist
        self.wordlist = load_wordlist(wordlist_file)
        self.logger.info(f"Loaded {len(self.wordlist)} words from wordlist")
        
        # Create context
        self.context = ScanContext(
            domain=domain,
            wordlist=self.wordlist,
            config={
                'concurrency': concurrency,
                'timeout': timeout,
                'stealth': stealth,
                'use_ai': use_ai,
                'use_permutation': use_permutation,
                'use_passive': use_passive,
                'output_format': output_format
            }
        )
        
        # Build pipeline
        self.pipeline = Pipeline(self.context)
        
        # Add stages dynamically
        if use_passive:
            self.pipeline.add_stage(PassiveStage())
        
        self.pipeline.add_stage(ActiveStage())
        
        if use_permutation or use_ai:
            self.pipeline.add_stage(GenerateStage())
        
        self.pipeline.add_stage(ValidateStage())
        self.pipeline.add_stage(ScoreStage())
        
        if output_file:
            self.pipeline.add_stage(OutputStage(output_file, output_format))
    
    async def run(self):
        """Run the entire scan"""
        self.print_banner()
        self.print_config()
        
        try:
            await self.pipeline.run()
            self.print_summary()
            return self.context
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    def print_banner(self):
        """Print ASCII banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      ████████╗███████╗██╗     ██╗         ██████╗ ███╗   ██╗ ███████╗
║      ╚══██╔══╝██╔════╝██║     ██║         ██╔══██╗████╗  ██║ ██╔════╝
║         ██║   █████╗  ██║     ██║         ██║  ██║██╔██╗ ██║ ███████╗
║         ██║   ██╔══╝  ██║     ██║         ██║  ██║██║╚██╗██║ ╚════██║
║         ██║   ███████╗███████╗███████╗    ██████╔╝██║ ╚████║ ███████║
║         ╚═╝   ╚══════╝╚══════╝╚══════╝    ╚═════╝ ╚═╝  ╚═══╝ ╚══════╝
║                                                               ║
║              🔍  Fast Subdomain Discovery  🔍                 ║
║                        v1.0.0                                ║
╚═══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_config(self):
        """Print configuration"""
        print(f"\n[*] Target: {self.domain}")
        print(f"[*] Wordlist: {len(self.wordlist)} words")
        print(f"[*] Concurrency: {self.context.config['concurrency']}")
        print(f"[*] Timeout: {self.context.config['timeout']}s")
        print(f"[*] Stealth: {self.context.config['stealth']}")
        print(f"[*] AI: {self.context.config['use_ai']}")
        print(f"[*] Permutation: {self.context.config['use_permutation']}")
        print(f"[*] Passive: {self.context.config['use_passive']}")
        print()
    
    def print_summary(self):
        """Print scan summary"""
        summary = self.context.get_summary()
        
        print("\n" + "="*55)
        print("SCAN SUMMARY")
        print("="*55)
        print(f"Domain: {summary['domain']}")
        print(f"Duration: {summary['duration_seconds']:.2f}s")
        print(f"Total found: {summary['total_found']}")
        print(f"  - Passive: {summary['passive_found']}")
        print(f"  - Active: {summary['active_found']}")
        print(f"  - Generated: {summary['generated_found']}")
        print(f"Query stats: {summary['successful_queries']}/{summary['total_queries']} ({summary['success_rate']})")
        
        if summary['total_found'] > 0:
            print(f"\n[+] Discovered subdomains ({summary['total_found']}):")
            for sub in sorted(self.context.discovered)[:30]:
                ips = self.context.get_ips(sub)
                ip_str = f" -> {', '.join(ips)}" if ips else ""
                print(f"    {sub}.{self.domain}{ip_str}")
            
            if len(self.context.discovered) > 30:
                print(f"    ... and {len(self.context.discovered) - 30} more")
