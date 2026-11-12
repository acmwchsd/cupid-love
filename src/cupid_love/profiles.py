import json
import os
from typing import Any
from pathlib import Path

Profile = dict[str, Any]

TRAITS = (
    "openness",  # 1 = loves routine          5 = always exploring
    "extraversion",  # 1 = quiet, recharges alone 5 = outgoing
    "agreeableness",  # 1 = blunt, independent     5 = gentle, accommodating
    "conscientiousness",  # 1 = spontaneous            5 = organized planner
    "emotional_steadiness",  # 1 = feels things deeply    5 = calm under pressure
    "romanticism",  # 1 = practical              5 = hopeless romantic
)
LIFESTYLES = ("quiet", "balanced", "lively")
COMMUNICATION_STYLES = ("direct", "gentle", "playful", "thoughtful")
RELATIONSHIP_GOALS = ("long_term", "casual", "friendship_first", "not_sure")
GENDERS = ("woman", "man", "helicopter")


def data_dir() -> Path:
    env = os.environ.get("CUPID_DATA_DIR")
    return Path(env) if env else Path(__file__).resolve().parents[2] / "data"


def load_profiles() -> list[Profile]:
    with open(data_dir() / "profiles.json", encoding="utf-8") as f:
        return json.load(f)


def get_profile(name_or_id: str) -> Profile | None:
    wanted = name_or_id.strip().lower()
    for p in load_profiles():
        if p["id"] == wanted or p["name"].lower() == wanted:
            return p
    return None


def search_profiles(
    interests: list[str] | None = None,
    gender: str | None = None,
    min_age: int | None = None,
    max_age: int | None = None,
) -> list[Profile]:
    wanted = {i.strip().lower() for i in interests or []}
    results = []
    for p in load_profiles():
        if wanted and not wanted & set(p["interests"]):
            continue
        if gender and p["gender"] != gender:
            continue
        if min_age and p["age"] < min_age:
            continue
        if max_age and p["age"] > max_age:
            continue
        results.append(p)
    return results


def summarize(p: Profile) -> str:
    label = " (fictional)" if p.get("fictional") else ""
    return f"{p['name']}, {p['age']}{label}: {', '.join(p['interests'][:4])}"


def new_profile(
    name: str,
    age: int,
    interests: list[str],
    values: list[str] | None = None,
    personality: dict[str, int] | None = None,
    lifestyle: str = "balanced",
    communication: str = "thoughtful",
    relationship_goal: str = "not_sure",
    gender: str | None = None,
    interested_in: list[str] | None = None,
    bio: str = "",
) -> Profile:
    if not name.strip():
        raise ValueError("name can't be empty.")
    if age < 18:
        raise ValueError("cupid is for adults only (18+).")
    if not interests:
        raise ValueError("add at least one interest.")
    traits = {t: 3 for t in TRAITS}
    for key, value in (personality or {}).items():
        if key not in TRAITS:
            raise ValueError(
                f"unknown personality traits '{key}'. use one of: {', '.join(TRAITS)}"
            )
        if not 1 <= int(value) <= 5:
            raise ValueError(f"{key} must be between 1 and 5.")
        traits[key] = int(value)
    for value, allowed, label in (
        (lifestyle, LIFESTYLES, "lifestyle"),
        (communication, COMMUNICATION_STYLES, "communication"),
        (relationship_goal, RELATIONSHIP_GOALS, "relationship_goal"),
    ):
        if value not in allowed:
            raise ValueError(f"{label} must be one of: {', '.join(allowed)}")
    if gender is not None and gender not in GENDERS:
        raise ValueError(f"gender must be one of: {', '.join(GENDERS)}")
    return {
        "id": "me",
        "name": name.strip(),
        "age": age,
        "gender": gender,
        "interested_in": interested_in or ["everyone"],
        "bio": bio.strip(),
        "interests": [i.strip().lower() for i in interests if i.strip()],
        "values": [v.strip().lower() for v in values or [] if v.strip()],
        "personality": traits,
        "lifestyle": lifestyle,
        "communication": communication,
        "relationship_goal": relationship_goal,
        "fictional": False,
    }


def load_my_profile() -> Profile | None:
    path = data_dir() / "me.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_my_profile(profile: Profile) -> Path:
    path = data_dir() / "me.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
    return path


def delete_my_profile() -> bool:
    path = data_dir() / "me.json"
    if path.exists():
        path.unlink()
        return True
    return False


if __name__ == "__main__":
    print(summarize(get_profile("marcus")))
    print(new_profile("Artanio Perlaro", 19, "football"))
