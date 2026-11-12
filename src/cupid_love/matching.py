from typing import Any
from .profiles import Profile, TRAITS, load_profiles

WEIGHTS = {
    "personality": 0.25,
    "interests": 0.25,
    "values_lifestyle": 0.25,
    "communication": 0.15,
    "relationship": 0.10,
}


def _overlap(a: list[str], b: list[str]) -> float:
    if not a or not b:
        return 0.0
    return len(set(a) & set(b)) / min(len(set(a)), len(set(b)))


def _personality(a: Profile, b: Profile) -> tuple[float, str]:
    sims = {t: 1 - abs(a["personality"][t] - b["personality"][t]) / 4 for t in TRAITS}
    close = [t.replace("_", " ") for t, s in sims.items() if s >= 0.75]
    reason = (
        f"Similar {', '.join(close[:3])}."
        if close
        else "Quite different personalities."
    )
    return sum(sims.values()) / len(sims), reason


def _interests(a: Profile, b: Profile) -> tuple[float, str]:
    shared = sorted(set(a["interests"]) & set(b["interests"]))
    reason = (
        f"Shared interests: {', '.join(shared)}."
        if shared
        else "No shared interests yet."
    )
    return _overlap(a["interests"], b["interests"]), reason


def _values_lifestyle(a: Profile, b: Profile) -> tuple[float, str]:
    values = _overlap(a["values"], b["values"])
    gap = abs(
        ["quiet", "balanced", "lively"].index(a["lifestyle"])
        - ["quiet", "balanced", "lively"].index(b["lifestyle"])
    )
    lifestyle = {0: 1.0, 1: 0.6, 2: 0.2}[gap]
    shared = sorted(set(a["values"]) & set(b["values"]))
    reason = f"Both value {', '.join(shared)}." if shared else "Different values."
    if gap == 0:
        reason += f" Both prefer {a['lifestyle']} surroundings."
    return 0.6 * values + 0.4 * lifestyle, reason


def _communication(a: Profile, b: Profile) -> tuple[float, str]:
    if a["communication"] == b["communication"]:
        return 1.0, f"Same communication style ({a['communication']})."
    return 0.6, f"Different styles: {a['communication']} and {b['communication']}."


def _relationship(a: Profile, b: Profile) -> tuple[float, str]:
    ga, gb = a["relationship_goal"], b["relationship_goal"]
    if ga == gb:
        return 1.0, f"Both looking for {ga.replace('_', ' ')}."
    if {ga, gb} == {"long_term", "casual"}:
        return 0.1, "One wants long-term, the other casual."
    return 0.6, f"Goals: {ga.replace('_', ' ')} and {gb.replace('_', ' ')}."


FACTORS = {
    "personality": _personality,
    "interests": _interests,
    "values_lifestyle": _values_lifestyle,
    "communication": _communication,
    "relationship": _relationship,
}


def compatibility(me: Profile, other: Profile) -> dict[str, Any]:
    """Score two profiles from 0 to 100, with a reason for every factor."""
    factors = []
    total = 0.0
    for name, fn in FACTORS.items():
        raw, reason = fn(me, other)
        score = round(raw * 100, 1)
        contribution = round(WEIGHTS[name] * score, 1)
        total += WEIGHTS[name] * score
        factors.append(
            {
                "factor": name,
                "weight": WEIGHTS[name],
                "score": score,
                "contribution": contribution,
                "reason": reason,
            }
        )
    return {
        "with": other["name"],
        "fictional": other.get("fictional", False),
        "score": round(total, 1),
        "shared_interests": sorted(set(me["interests"]) & set(other["interests"])),
        "factors": factors,
        "note": "An estimate from self-reported answers, not a prediction.",
    }


def wants(seeker: Profile, other: Profile) -> bool:
    """Does `seeker` want to meet someone of `other`'s gender? Unknown = yes."""
    prefs = set(seeker.get("interested_in") or ["everyone"])
    gender = other.get("gender")
    if "everyone" in prefs or gender is None:
        return True
    return {"woman": "women", "man": "men", "non_binary": "non_binary"}[gender] in prefs


def best_matches(
    me: Profile, limit: int = 3, candidates: list[Profile] | None = None
) -> list[dict[str, Any]]:
    """Rank candidates by compatibility, keeping only mutual gender preferences."""
    pool = candidates if candidates is not None else load_profiles()
    results = [
        compatibility(me, p)
        for p in pool
        if p["id"] != me.get("id") and wants(me, p) and wants(p, me)
    ]
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:limit]
