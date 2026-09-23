# Capstone-Project  

api/ — the front door
- main.py — wires everything together; this is what actually runs when a request comes in
- settings.py — app-level settings (API keys, ports, env variables)

config/ — the rulebook, as data
- constitution.yaml — the actual policy rules (what's allowed, blocked, flagged)
- failure_modes.yaml — what to do if a check times out or errors (block vs. allow)

cost/ — figures out what things cost
- calibration/calibration.py — script to refresh cost numbers from real usage data
- breakeven.py — checks whether the safety/routing overhead itself is costing more than it saves
- estimator.py — estimates energy/dollar cost for a given request + tier
- model_registry.py — lookup table of cost info per model/GPU combo

guardrails/ — the security layer
- adversarial/classifier_attack_suite.py — test inputs designed to trick the triage classifier
- adversarial/router_attack_suite.py — test inputs designed to trick the router into a weaker path
- injection_screen.py — catches prompt injection / jailbreak attempts before anything else runs
- output_filter.py — checks the final output for unsafe content

interface/ — what the user sees
- confidence.py — shows how reliable a given answer is, so the user knows how much to trust it
- feedforward.py — tells the user what's about to happen before it happens (which tier, why)
- human_checkpoint.py — the "are you sure / please confirm" step for high-stakes requests

llm/ — talks to the actual AI models
- gateway.py — the raw API client (handles auth, retries, request/response format)

audit/ — keeps a record
- audit_log.py — logs every decision made and why
- metrics.py — tracks numbers over time (cost saved, escalation rate, etc.)

policy/ — enforces the rulebook
- engine.py — reads constitution.yaml and actually applies the rules
- schemas.py — defines the shared data shapes (what a "decision" or "classification" looks like)
- governance/CODEOWNERS — says who must approve changes to the policy files
- governance/change_log.py — keeps a version history of policy changes

session/ — remembers context across a conversation
- prefilter.py — quick check for "have we already answered this exact thing"
- session_state.py — tracks cumulative risk/cost across a whole conversation, not just one message

tests/
- test.py — placeholder test file (to be split into per-module test folders as those get built)

tiers/ — the actual ways to answer a request, cheapest to priciest
- cache_lookup.py — return a previously-saved answer
- deterministic.py — rule-based / calculator / lookup answers, no AI involved
- small_classifier.py — a small, cheap model for simple categorization tasks
- rag_small_model.py — a small model with retrieved reference info to back its answer
- llm_call.py — calls the full LLM (via llm/gateway.py), with adjustable reasoning depth

triage/ — decides what kind of request this is and where it should go
- bias_monitor.py — checks the router isn't treating some phrasing/languages unfairly
- classifier.py — figures out what type of request this is (lookup, generation, judgment, etc.)
- decision.py — the actual scoring logic that picks which tier handles the request
- modality_router.py — handles the fact that text/image/audio requests need different treatment
- taxonomy.py — defines the categories used to classify requests

validation/ — checks the answer before it's shown to anyone
- non_llm_checks.py — cheap, rule-based checks (preferred over using another AI call to check)
- validator.py — the main validation logic; runs quality/safety/confidence checks on output

escalation/
- repair_router.py — decides what happens when a stage fails — retry, escalate to a bigger tier, or hand to a human

Root files
- README.md — explains what the project is and how to run it
- requirements.txt — list of Python packages the project needs
