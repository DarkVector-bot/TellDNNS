"""
OutputStage - Format and save results
"""

import json
from pathlib import Path
from datetime import datetime

from .base import BaseStage
from ..utils.logger import get_logger


class OutputStage(BaseStage):
    """Output results to file"""
    
    def __init__(self, output_file: str, output_format: str = "txt"):
        self.output_file = output_file
        self.output_format = output_format
        self.logger = get_logger()
    
    async def run(self, context):
        """Save results to file"""
        domain = context.domain
        discovered = sorted(context.discovered)
        validated = context.validated
        scores = context.metadata.get('scores', {})
        
        self.logger.info(f"Saving results to {self.output_file} ({self.output_format})")
        
        # Create output directory if needed
        output_path = Path(self.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.output_format == "json":
            self._save_json(context, output_path)
        else:
            self._save_txt(context, output_path)
        
        self.logger.info(f"Results saved to {self.output_file}")
        
        # Also print to console
        print(f"\n[+] Discovered {len(discovered)} subdomains:")
        for sub in discovered[:20]:
            ips = validated.get(sub, [])
            ip_str = f" -> {', '.join(ips)}" if ips else ""
            score = scores.get(sub, 0)
            print(f"    [{score}] {sub}.{domain}{ip_str}")
        
        if len(discovered) > 20:
            print(f"    ... and {len(discovered) - 20} more")
        
        return True
    
    def _save_json(self, context, output_path: Path):
        """Save as JSON"""
        data = {
            'tool': 'TellDNS',
            'version': '1.0.0',
            'target': context.domain,
            'scan_start': context.start_time.isoformat(),
            'scan_end': datetime.now().isoformat(),
            'summary': context.get_summary(),
            'subdomains': []
        }
        
        for sub in sorted(context.discovered):
            ips = context.validated.get(sub, [])
            entry = {
                'subdomain': sub,
                'full_domain': f"{sub}.{context.domain}",
                'ips': ips,
                'source': context.metadata.get(sub, {}).get('source', 'unknown'),
                'score': context.metadata.get('scores', {}).get(sub, 0)
            }
            data['subdomains'].append(entry)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _save_txt(self, context, output_path: Path):
        """Save as plain text"""
        with open(output_path, 'w') as f:
            f.write(f"TellDNS Scan Results - {context.domain}\n")
            f.write(f"Started: {context.start_time.isoformat()}\n")
            f.write(f"Completed: {datetime.now().isoformat()}\n")
            f.write("="*50 + "\n\n")
            
            for sub in sorted(context.discovered):
                ips = context.validated.get(sub, [])
                ip_str = f" -> {', '.join(ips)}" if ips else ""
                f.write(f"{sub}.{context.domain}{ip_str}\n")
