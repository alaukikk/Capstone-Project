"""
Tier 0: Cache lookup.

The cache is checked before any deterministic logic, retrieval, small-model,
or LLM work. For now this is an in-memory cache so the runtime can be tested
without adding Redis or another external dependency.
"""

from hashlib import sha256
from typing import Optional


# Simple process-local cache.
# Key: normalized request hash
# Value: previously generated response
_CACHE: dict[str, str] = {}


def _normalize_request(request_text: str) -> str:
    """Normalize a request so trivial formatting differences still hit cache."""
    return " ".join(request_text.strip().lower().split())


def _cache_key(request_text: str) -> str:
    """Create a stable, non-reversible key for the normalized request."""
    normalized = _normalize_request(request_text)
    return sha256(normalized.encode("utf-8")).hexdigest()


def get_cached_response(request_text: str) -> Optional[str]:
    """
    Return a previously cached response if one exists.

    Returns:
        The cached response on a cache hit, otherwise None.
    """
    if not request_text or not request_text.strip():
        return None

    return _CACHE.get(_cache_key(request_text))


def cache_response(request_text: str, response: str) -> None:
    """
    Store a response for a request.

    This will later be replaceable with a persistent cache such as Redis
    without changing the tier's public interface.
    """
    if not request_text or not request_text.strip():
        return

    if not response:
        return

    _CACHE[_cache_key(request_text)] = response


def clear_cache() -> None:
    """Clear the process-local cache. Mainly useful for testing."""
    _CACHE.clear()
