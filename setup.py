#!/usr/bin/env python3
"""
Setup script for TellDNS
"""

from setuptools import setup, find_packages
import os

# Read version
version = "1.0.0"

# Read README
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_path, 'r') as f:
    long_description = f.read()

# Read requirements
req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(req_path, 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="telldns",
    version=version,
    description="TellDNS - Fast Subdomain Discovery Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DarkVector-bot",
    author_email="darkvector@example.com",
    url="https://github.com/DarkVector-bot/TellDNS",
    license="MIT",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "telldns = telldns.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Internet :: Name Service (DNS)",
    ],
    python_requires=">=3.9",
    keywords="subdomain, dns, enumeration, bugbounty, security",
    project_urls={
        "Bug Reports": "https://github.com/DarkVector-bot/TellDNS/issues",
        "Source": "https://github.com/DarkVector-bot/TellDNS",
    },
)
