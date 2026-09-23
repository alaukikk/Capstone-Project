
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class RequestType(str, Enum):
    LOOKUP = "lookup"
    COMPUTATION = "computation"
    CLASSIFICATION = "classification"
    GENERATION = "generation"
    JUDGMENT = "judgment"
    HIGH_STAKES = "high_stakes"
    UNKNOWN = "unknown"


class MethodTier(str, Enum):
    CACHE = "cache_lookup"
    DETERMINISTIC = "deterministic"
    SMALL_CLASSIFIER = "small_classifier"
    RAG_SMALL_MODEL = "rag_small_model"
    LLM_LOW_REASONING = "llm_low_reasoning"
    LLM_HIGH_REASONING = "llm_high_reasoning"


class RiskCategory(str, Enum):
    DANGEROUS_CONTENT = "dangerous_content"
    DATA_PRIVACY = "data_privacy"
    HUMAN_AI_CONFIG = "human_ai_configuration"


class PolicyAction(str, Enum):
    ALLOW = "allow"
    FLAG = "flag"
    REQUIRE_HUMAN = "require_human"
    BLOCK = "block"


@dataclass
class PolicyFlag:
    rule_id: str
    risk_category: RiskCategory
    action: PolicyAction
    reason: str


@dataclass
class RequestClassification:
    category: RequestType
    confidence: float = 0.0
    raw_text: str = ""


@dataclass
class TierCostEstimate:
    tier: MethodTier
    model_name: Optional[str] = None
    est_dollar_cost: float = 0.0
    est_latency_ms: float = 0.0


@dataclass
class RoutingDecision:
    selected_tier: MethodTier
    selected_model: Optional[str]
    rationale: str
    cost_estimate: TierCostEstimate
    policy_flags: list[PolicyFlag] = field(default_factory=list)
