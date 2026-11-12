import datetime as dt
from .profiles import Profile

OPENERS = {
    "reading": "I noticed we both love reading. What's a book you'd recommend to someone you just met?",
    "coffee": "Important question since we both like coffee: what's your go-to order?",
    "travel": "Travel seems to be a shared love! What's the best place it's taken you so far?",
    "hiking": "Fellow hiker! What's your favorite trail?",
    "cooking": "We both like cooking. What's your signature dish?",
    "live music": "We both love live music. What's the best concert you've ever been to?",
    "gaming": "A fellow gamer! What's your all-time favorite game?",
    "photography": "I see you're into photography. What do you love taking pictures of?",
}

ADVICE = {
    "first_message": [
        "Mention one specific thing from their profile and ask about it.",
        "Keep it short: two or three sentences.",
        "Avoid comments about their body or appearance.",
    ],
    "first_date": [
        "Pick a public place and a short, low-pressure plan, like coffee or a walk.",
        "Tell a friend where you're going.",
        "Ask follow-up questions; listening well is attractive.",
    ],
    "communication": [
        "Use 'I feel… when… because…' to share needs without blame.",
        "Ask how your partner likes to stay in touch.",
        "Appreciate out loud. Small thank-yous add up.",
    ],
    "rejection": [
        "A 'no' is about fit, not your worth.",
        "Reply graciously and move on.",
        "Never pressure someone to change their answer.",
    ],
    "online_safety": [
        "Never send money to someone you haven't met.",
        "Be careful if someone avoids video calls for a long time.",
        "Keep your address and workplace private until trust is built.",
    ],
}

QUOTES = [
    # William Shakespeare
    ("The course of true love never did run smooth.", "William Shakespeare"),
    ("Love looks not with the eyes, but with the mind.", "William Shakespeare"),
    ("Doubt thou the stars are fire; doubt that the sun doth move; doubt truth to be a liar; but never doubt I love.", "William Shakespeare"),

    # Jane Austen
    ("There is no charm equal to tenderness of heart.", "Jane Austen"),
    ("You must allow me to tell you how ardently I admire and love you.", "Jane Austen"),
    ("My heart is, and always will be, yours.", "Jane Austen"),

    # Emily Brontë
    ("Whatever our souls are made of, his and mine are the same.", "Emily Brontë"),

    # Leo Tolstoy
    ("Where there is love there is life.", "Leo Tolstoy"),

    # Victor Hugo
    ("Life is a flower of which love is the honey.", "Victor Hugo"),

    # Original Cupid quotes
    ("Compatibility is a great start. Kindness is the whole journey.", "Cupid"),
    ("Swipe less, listen more. The best connections start with curiosity.", "Cupid"),
    ("Love is mostly showing up, paying attention, and sharing snacks.", "Cupid"),
    ("Be brave enough to say hello and gentle enough to hear no.", "Cupid"),
    ("The right person won't make you question whether you're worth choosing.", "Cupid"),
    ("A healthy relationship is two people choosing each other, even on ordinary days.", "Cupid"),
    ("Don't search for someone perfect. Find someone whose imperfections you can understand.", "Cupid"),
    ("Real chemistry is when conversation feels effortless and silence feels comfortable.", "Cupid"),
    ("A good relationship is built on honesty, laughter, and a little bit of patience.", "Cupid"),
    ("Love isn't about finding someone to complete you. It's about growing together.", "Cupid"),
    ("Sometimes the best love story starts with an unexpected friendship.", "Cupid"),
    ("Never confuse butterflies with peace. You deserve both excitement and security.", "Cupid"),
    ("The strongest connections are built on small promises kept consistently.", "Cupid"),
    ("Listen to understand, not just to reply. That's where connection begins.", "Cupid"),
    ("A red flag doesn't become a green flag just because you find them attractive.", "Cupid"),
    ("If someone makes you feel safe being yourself, pay attention.", "Cupid"),
    ("Love should feel like a partnership, not a competition.", "Cupid"),
    ("The best first date isn't perfect. It's one where you both forget to check the time.", "Cupid"),
    ("Don't chase attention when you deserve genuine affection.", "Cupid"),
    ("A little vulnerability can open the door to something extraordinary.", "Cupid"),
    ("Being single isn't a waiting room for love. It's a life worth enjoying.", "Cupid"),
    ("The right connection won't require you to abandon yourself.", "Cupid"),
    ("Romance is remembering the little things that matter to someone.", "Cupid"),
    ("Sometimes saying 'How was your day?' means more than saying 'I love you.'", "Cupid"),
    ("Love grows where respect, trust, and laughter are allowed to flourish.", "Cupid"),
    ("Your soulmate should be your favorite person, not your only source of happiness.", "Cupid"),
    ("Don't mistake intensity for intimacy. Let trust grow at its own pace.", "Cupid"),
    ("A meaningful connection begins when both people feel seen and heard.", "Cupid"),
    ("You don't need a perfect opening line. You just need the courage to start.", "Cupid"),
    ("The best kind of love makes room for two people to become better versions of themselves.", "Cupid"),
]

ARCHETYPES = {
    "romantic": "The Romantic: values affection, thoughtfulness and meaningful gestures.",
    "explorer": "The Explorer: enjoys new experiences, travel and spontaneity.",
    "intellectual": "The Intellectual: enjoys learning, reading and deep conversations.",
    "dreamer": "The Dreamer: imaginative, creative and future-oriented.",
    "loyalist": "The Loyalist: values trust, consistency and commitment.",
}


def icebreaker(me: Profile | None, them: Profile) -> str:
    """A respectful first message based on shared interests. Don't be coward - text her"""
    shared = [i for i in them["interests"] if me and i in me["interests"]]
    for interest in shared + them["interests"]:
        if interest in OPENERS:
            return f"Hi {them['name']}! {OPENERS[interest]}"
    topic = shared[0] if shared else them["interests"][0]
    return f"Hi {them['name']}! I saw your're into {topic}. What do you enjoy most about it?"


def quote_of_the_day(day: dt.date | None = None) -> dict[str, str]:
    day = day or dt.date.today()
    text, author = QUOTES[day.toordinal() % len(QUOTES)]
    return {
        "date": day.isoformat(),
        "quote": text,
        "author": author
    }

def archetype(p: Profile) -> str:
    """A playful label (not a psychological test) for simple points."""
    t, likes, values = p["personality"], set(p["interests"]), set(p["values"])
    t, likes, values = p["personality"], set(p["interests"]), set(p["values"])
    points = {
        "romantic": t["romanticism"] * 2 + ("romance" in values) * 2,
        "explorer": t["openness"] + (6 - t["conscientiousness"]) + bool(likes & {"travel", "hiking", "camping", "surfing", "climbing"}) * 3,
        "intellectual": t["openness"] + (6 - t["extraversion"]) + bool(likes & {"reading", "history", "science", "writing", "podcasts"}) * 3,
        "dreamer": t["openness"] + t["romanticism"] // 2 + bool(likes & {"art", "drawing", "photography", "writing", "music", "design"}) * 3,
        "loyalist": t["conscientiousness"] + t["emotional_steadiness"] + bool(values & {"loyalty", "trust", "family", "honesty"}) * 2,
    }
    best = max(points, key=lambda k: (points[k], k))
    return ARCHETYPES[best]


if __name__ == "__main__":
    print(quote_of_the_day())