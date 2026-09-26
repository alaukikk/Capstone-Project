
# Have we already answered this exact question before? #

from typing import Optional


def try_cache_lookup(request_text: str) -> Optional[str]:
    """Returns None until real cache (Redis-backed) lookup is wired up."""
    return None
