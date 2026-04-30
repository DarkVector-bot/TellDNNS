"""
Tests for DNS resolver
"""

import pytest
import asyncio
from telldns.network.resolver import DNSResolver


@pytest.mark.asyncio
async def test_resolver_valid():
    """Test resolving valid domain"""
    resolver = DNSResolver(timeout=3.0, stealth=False)
    result = await resolver.resolve("google.com")
    assert result is not None
    assert len(result) > 0


@pytest.mark.asyncio
async def test_resolver_invalid():
    """Test resolving invalid domain"""
    resolver = DNSResolver(timeout=2.0, stealth=False)
    result = await resolver.resolve("this-domain-should-not-exist-12345.com")
    assert result is None


@pytest.mark.asyncio
async def test_resolver_timeout():
    """Test resolver timeout"""
    resolver = DNSResolver(timeout=0.1, stealth=False)
    result = await resolver.resolve("example.com")
    # May timeout or succeed, both acceptable
    assert result is None or isinstance(result, list)
