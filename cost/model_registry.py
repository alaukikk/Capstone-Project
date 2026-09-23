
from dataclasses import dataclass


@dataclass
class ModelInfo:
    name: str                    # Model name #
    provider: str                # Company that provides it #
    cost_per_1k_tokens: float    # How much it costs per 1k tokens #
    typical_latency_ms: float    # How long it tyoically takes to respond #
    capability_score: float      # A how good is it score #


MODEL_CATALOG: list[ModelInfo] = [
    ModelInfo("stub-small", "stub", 0.0001, 200, 0.4),
    ModelInfo("stub-medium", "stub", 0.001, 600, 0.7),
    ModelInfo("stub-large", "stub", 0.01, 1500, 0.95),
]
