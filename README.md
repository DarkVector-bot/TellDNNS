# TellDNNS
TellDNS is a high-performance subdomain discovery engine combining passive enumeration, active bruteforce, AI prediction, and permutation attacks. Features stealth mode, async DNS, and JSON output. Lightweight &amp; powerful.


---

📝 Short Description (GitHub - max 350 chars)

```
TellDNS is a powerful subdomain discovery engine that reveals hidden assets through passive enumeration, active bruteforce, AI prediction, and permutation attacks. Stealth mode, async DNS, JSON output. Built for bug hunters & security researchers.
```

---

📝 Long Description + Usage (For README.md)

```markdown
# 🔍 TellDNS - Tell Me Your Subdomains

**TellDNS** is a next-generation subdomain discovery engine designed to uncover hidden assets of any domain. Combines 5+ enumeration techniques in one efficient and deadly pipeline.

> "The quieter you become, the more you are able to hear." - TellDNS Stealth Mode

---

## ⚡ Quick Start

```bash
# Install in 10 seconds
git clone https://github.com/DarkVector-bot/TellDNS.git
cd TellDNS
pip install -r requirements.txt

# Scan a domain
python -m telldns -d example.com

# Output:
# [*] Target: example.com
# [+] Discovered 47 subdomains:
#     www.example.com -> 93.184.216.34
#     mail.example.com -> 93.184.216.34
#     admin.example.com -> 192.0.2.10
#     api.example.com -> 192.0.2.20
#     ... and 43 more
```

---

🎯 Usage Guide

1. Basic Scan - For beginners

```bash
python -m telldns -d target.com
```

Just enter the domain, TellDNS does:

· ✅ Passive scan from 5+ sources (crt.sh, AlienVault, etc.)
· ✅ Active bruteforce with 500+ default words
· ✅ Automatic DNS validation

2. Stealth Mode - For bug bounty (🌟 recommended)

```bash
python -m telldns -d target.com --stealth -o results.json
```

· ✅ Random delays (avoid rate limiting)
· ✅ DNS resolver rotation every 50 queries
· ✅ Results saved to JSON file

3. Full Power - Maximum results

```bash
python -m telldns -d target.com --stealth -c 1000 -o full_scan.json
```

· ✅ 1000 queries/second concurrency
· ✅ All features active (passive + active + AI + permutation)

4. Custom Wordlist - For specific targets

```bash
python -m telldns -d target.com -w my_wordlist.txt --stealth
```

5. Quick Scan - Bruteforce only (no passive)

```bash
python -m telldns -d target.com --no-passive
```

6. Verbose Mode - See everything happening

```bash
python -m telldns -d example.com -v
```

---

📊 Output Examples

Terminal Output (Default)

```
╔═══════════════════════════════════════════════════════════════╗
║                    TellDNS v1.0.0                            ║
║              🔍  Fast Subdomain Discovery  🔍                 ║
╚═══════════════════════════════════════════════════════════════╝

[*] Target: example.com
[*] Wordlist: 542 words
[*] Concurrency: 500
[*] Stealth: true

[1/5] Running stage: PassiveStage
[*] Passive scan from crt.sh...
[+] Found 23 subdomains from passive sources

[2/5] Running stage: ActiveStage
[*] Active bruteforce with 542 words...
  [+] mail.example.com -> 93.184.216.34
  [+] www.example.com -> 93.184.216.34
  [+] admin.example.com -> 192.0.2.10

===================================================
SCAN SUMMARY
===================================================
Domain: example.com
Duration: 12.34s
Total found: 47
  - Passive: 23
  - Active: 18
  - Generated: 6
```

JSON Output (with -o results.json)

```json
{
  "tool": "TellDNS",
  "version": "1.0.0",
  "target": "example.com",
  "scan_start": "2026-01-15T10:30:00",
  "total_found": 47,
  "subdomains": [
    {
      "subdomain": "www",
      "full_domain": "www.example.com",
      "ips": ["93.184.216.34"],
      "source": "active",
      "score": 85
    },
    {
      "subdomain": "mail",
      "full_domain": "mail.example.com",
      "ips": ["93.184.216.34"],
      "source": "passive",
      "score": 70
    }
  ]
}
```

---

🛠️ All Commands (Reference)

Command Description
-d, --domain Target domain (required)
-o, --output Save results to file
-w, --wordlist Custom wordlist file
-c, --concurrency Parallel queries (default: 500)
-t, --timeout DNS timeout in seconds (default: 3)
--stealth Enable stealth mode (avoid detection)
--json Output in JSON format
--no-passive Disable passive sources
--no-ai Disable AI prediction
--no-permutation Disable permutation attack
-v, --verbose Show detailed process

---

🎓 Real-World Scenarios

Scenario 1: Bug Bounty Program

```bash
python -m telldns -d redacted.com --stealth -o bounty_results.json
```

Scenario 2: Internal Network Assessment

```bash
python -m telldns -d internal.company.local -c 1000 --no-stealth
```

Scenario 3: Target with Custom Wordlist

```bash
python -m telldns -d target.com -w wordlists/deep_50k.txt --stealth -c 800
```

Scenario 4: Quick Check (No Passive)

```bash
python -m telldns -d target.com --no-passive --no-ai
```

Scenario 5: Maximum Stealth (Slow but Invisible)

```bash
python -m telldns -d target.com --stealth -c 100 -t 5
```

---

📈 Performance

Mode Speed Detection Risk Best For
Default Fast Medium General use
Stealth Medium Low Bug bounty
Aggressive Very Fast High Internal networks
Max Stealth Slow Very Low Sensitive targets

---

🔧 Requirements

· Python 3.9+
· Internet connection (for DNS queries)
· 50MB free disk space

---

📦 Installation Options

Option 1: Direct Install

```bash
pip install -r requirements.txt
python -m telldns -d example.com
```

Option 2: Install as Package

```bash
pip install -e .
telldns -d example.com
```

Option 3: Using Make

```bash
make install
make run
```

---

⚡ Pro Tips

1. Always use --stealth for bug bounty - You don't want to trigger WAF alerts
2. Save results with -o - You'll thank yourself later
3. Use -v first time - Understand what's happening
4. Custom wordlists matter - Default is good, but specific wordlists find more
5. Combine with other tools - TellDNS for subdomains, then Nuclei for vulnerabilities

---

🆘 Need Help?

```bash
# Show all commands
python -m telldns --help

# Verbose mode for debugging
python -m telldns -d example.com -v
```

---

⭐ Star This Repo

If TellDNS helped you find hidden subdomains, give it a star! ⭐

---

Made with ❤️ for bug bounty hunters & security researchers

```

---

## ✅ **Ready to copy-paste to your GitHub README.md**
