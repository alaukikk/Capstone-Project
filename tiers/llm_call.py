
# Most expensive. LLM gets called #

def call_llm(request_text: str, model_name: str = "stub-model") -> str:
    """Fake response so the pipeline runs end-to-end before real model integration exists."""
    return f"[STUB LLM RESPONSE] would have called {model_name} for: {request_text[:50]!r}"
