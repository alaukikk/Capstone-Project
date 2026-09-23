
# Cheapest tier. If we've already answered this exact question before, just return the saved answer instead of doing any real work again.
from typing import Optional


def get_cached_response(request_text: str) -> Optional[str]:
    """Always a cache miss for now — real caching arrives Sprint 2."""
    return None
