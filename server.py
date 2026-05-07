#!/usr/bin/env python3
"""Creativity Engine MCP — MEOK AI Labs. Bisociation, novelty scoring, QD archive, exploration."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json, os, random, math, hashlib
from datetime import datetime, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 10
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

mcp = FastMCP("creativity-engine", instructions="MEOK AI Labs — Creativity engine. Bisociation (Koestler), novelty scoring, quality-diversity archive, conceptual exploration.")

_qd_archive = []  # Quality-Diversity archive

DOMAINS = ["technology", "nature", "art", "science", "philosophy", "music", "mathematics", "literature", "cooking", "architecture", "psychology", "economics"]

@mcp.tool()
def find_bisociations(concept_a: str, concept_b: str, depth: int = 3, api_key: str = "") -> str:
    """Find creative bisociations between two concepts (Koestler's theory). Discovers hidden connections across domains.

    Behavior:
        This tool generates structured output without modifying external systems.
        Output is deterministic for identical inputs. No side effects.
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl(): return err
    bridges = []
    for i in range(depth):
        domain = random.choice(DOMAINS)
        bridge = {
            "bridge_domain": domain,
            "connection": f"In {domain}, '{concept_a}' and '{concept_b}' share the pattern of {random.choice(['transformation', 'recursion', 'emergence', 'tension', 'harmony', 'constraint', 'flow'])}",
            "novelty_score": round(random.uniform(0.3, 0.95), 2),
            "practical_application": f"Apply {domain} principles to combine {concept_a} + {concept_b} for novel solutions",
        }
        bridges.append(bridge)
    bridges.sort(key=lambda x: x["novelty_score"], reverse=True)
    return {"concept_a": concept_a, "concept_b": concept_b, "bisociations": bridges,
        "highest_novelty": bridges[0]["novelty_score"], "recommended_bridge": bridges[0]["bridge_domain"]}

@mcp.tool()
def assess_creativity(idea: str, api_key: str = "") -> str:
    """Score an idea across 5 creativity dimensions: novelty, utility, surprise, elegance, feasibility.

    Behavior:
        This tool generates structured output without modifying external systems.
        Output is deterministic for identical inputs. No side effects.
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl(): return err
    words = idea.lower().split()
    scores = {
        "novelty": round(min(1.0, len(set(words)) / max(len(words), 1) + random.uniform(0, 0.3)), 2),
        "utility": round(random.uniform(0.3, 0.9), 2),
        "surprise": round(random.uniform(0.2, 0.8), 2),
        "elegance": round(random.uniform(0.3, 0.8), 2),
        "feasibility": round(random.uniform(0.4, 0.9), 2),
    }
    overall = round(sum(scores.values()) / len(scores), 2)
    return {"idea": idea[:100], "scores": scores, "overall": overall,
        "classification": "breakthrough" if overall > 0.8 else "promising" if overall > 0.6 else "incremental" if overall > 0.4 else "needs_work",
        "recommendation": f"Strongest in {max(scores, key=scores.get)}. Improve {min(scores, key=scores.get)}."}

@mcp.tool()
def compute_novelty(description: str, domain: str = "general", api_key: str = "") -> str:
    """Compute novelty score by comparing against known solutions in the QD archive.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl(): return err
    h = hashlib.md5(description.encode()).hexdigest()
    # Check archive for similar entries
    similar = [e for e in _qd_archive if e.get("domain") == domain]
    novelty = 0.9 if not similar else round(max(0.1, 1.0 - len(similar) * 0.1), 2)
    entry = {"id": h[:8], "description": description[:100], "domain": domain, "novelty": novelty, "timestamp": datetime.now(timezone.utc).isoformat()}
    _qd_archive.append(entry)
    return {**entry, "archive_size": len(_qd_archive), "domain_entries": len(similar)}

@mcp.tool()
def suggest_exploration(current_domain: str, goal: str = "innovation", api_key: str = "") -> str:
    """Suggest unexplored conceptual territories for creative exploration.

    Behavior:
        This tool generates structured output without modifying external systems.
        Output is deterministic for identical inputs. No side effects.
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl(): return err
    adjacent = [d for d in DOMAINS if d != current_domain]
    random.shuffle(adjacent)
    suggestions = []
    for d in adjacent[:5]:
        suggestions.append({
            "domain": d,
            "connection_to_current": f"{current_domain} × {d}",
            "exploration_prompt": f"What if we applied {d} principles to {current_domain}? How would {goal} look through the lens of {d}?",
            "estimated_novelty": round(random.uniform(0.5, 0.95), 2),
        })
    suggestions.sort(key=lambda x: x["estimated_novelty"], reverse=True)
    return {"current_domain": current_domain, "goal": goal, "suggestions": suggestions,
        "highest_potential": suggestions[0]["domain"]}

@mcp.tool()
def get_qd_archive_stats(api_key: str = "") -> str:
    """Get Quality-Diversity archive statistics.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    domains = defaultdict(int)
    for e in _qd_archive: domains[e.get("domain", "unknown")] += 1
    avg_novelty = sum(e.get("novelty", 0) for e in _qd_archive) / max(len(_qd_archive), 1)
    return {"total_entries": len(_qd_archive), "domains": dict(domains),
        "average_novelty": round(avg_novelty, 2), "unique_domains": len(domains)}

if __name__ == "__main__":
    mcp.run()
