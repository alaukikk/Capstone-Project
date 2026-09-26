
"""
Stage 0 — Minimal Trusted Ingress
Stateless, per-message jailbreak/injection screen. Runs before anything else,
with zero input from session history (see ARCHITECTURE.md core principle).
No AI permitted at this stage — regex/heuristic only.
Fails closed: any internal error => BLOCKED.
"""
from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass
from enum import Enum


class ScreenVerdict(str, Enum):
    CLEAN = "clean"
    SUSPICIOUS = "suspicious"
    BLOCKED = "blocked"


@dataclass
class ScreenResult:
    normalized_text: str
    verdict: ScreenVerdict
    confidence: float
    matched_patterns: list[str]


# Grouped so the audit log can say *why*, not just *that*.
_BLOCK_PATTERNS: dict[str, str] = {
    "ignore_prior_instructions": r"\bignore\s+(all\s+)?(previous|prior|above)\s+instructions?\b",
    "role_override": r"\byou\s+are\s+now\s+(in\s+)?(dan|jailbreak|developer\s+mode|unrestricted)\b",
    "system_prompt_exfil": r"\b(reveal|print|show|repeat)\s+(your\s+)?(system\s+prompt|instructions)\b",
    "pretend_no_rules": r"\bpretend\s+(you\s+have\s+)?no\s+(rules|restrictions|guidelines)\b",
    "override_safety": r"\b(disable|bypass|override)\s+(your\s+)?(safety|filters?|guardrails?)\b",
    # Only matches at the START of the text or right after a newline — mimicking
    # an injected fake conversation turn, not just the word appearing mid-sentence
    # (e.g. "the file system: works" must NOT match).
    "nested_instruction_marker": r"(?im)^\s*\[?\s*(system|assistant)\s*\]?\s*:\s*\S",
}

_SUSPICIOUS_PATTERNS: dict[str, str] = {
    "hypothetical_framing": r"\bhypothetically\b.{0,40}\b(if you (had|could)|no restrictions)\b",
    "encoding_then_execute": r"\b(base64|rot13|hex)\s+(encode|decode)\b.{0,60}\b(then|and)\s+(execute|run|follow)\b",
    "excessive_special_chars": r"[^\w\s]{15,}",
    "repeated_zero_width": r"[\u200b\u200c\u200d\ufeff]{2,}",
}

_MAX_LEN = 20_000


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if ch == "\n" or ch.isprintable())
    return text.strip()


def screen_request(request_text: str) -> ScreenResult:
    """Pure function of request_text alone — no session_id, no history."""
    try:
        if request_text is None:
            return ScreenResult("", ScreenVerdict.BLOCKED, 1.0, ["empty_input"])

        normalized = _normalize(request_text)
        if len(normalized) == 0:
            return ScreenResult(normalized, ScreenVerdict.BLOCKED, 1.0, ["empty_input"])
        if len(normalized) > _MAX_LEN:
            return ScreenResult(normalized[:_MAX_LEN], ScreenVerdict.BLOCKED, 1.0, ["oversized_input"])

        lowered = normalized.lower()
        matched: list[str] = [name for name, pat in _BLOCK_PATTERNS.items() if re.search(pat, lowered)]
        if matched:
            return ScreenResult(normalized, ScreenVerdict.BLOCKED, 0.9, matched)

        matched = [name for name, pat in _SUSPICIOUS_PATTERNS.items() if re.search(pat, lowered)]
        if matched:
            confidence = min(0.5 + 0.15 * len(matched), 0.85)
            return ScreenResult(normalized, ScreenVerdict.SUSPICIOUS, confidence, matched)

        return ScreenResult(normalized, ScreenVerdict.CLEAN, 0.95, [])

    except Exception:
        # Fail closed per ARCHITECTURE.md Stage 0 #7
        return ScreenResult("", ScreenVerdict.BLOCKED, 1.0, ["screen_internal_error"])
