import re
from collections import Counter, defaultdict

from rules import (
    SHORT_REPLY_WORD_LIMIT,
    RECENT_MESSAGE_COUNT,
    CATEGORY_WEIGHTS,
    RED_FLAG_RATIO_CAUTION,
    RED_FLAG_RATIO_LEAVE,
    ESCALATION_THRESHOLD,
    VAGUE_INTENT_PHRASES,
    FRIEND_ZONE_PHRASES,
    DEFLECTION_PHRASES,
    BLAME_SHIFTING_PHRASES,
    LACK_OF_ACCOUNTABILITY_PHRASES,
    EMOTIONAL_UNAVAILABILITY_PHRASES,
    INCONSISTENCY_PHRASES,
    GASLIGHTING_PHRASES,
    CONTROL_OR_DISMISSAL_PHRASES,
)

PHRASE_BANKS = {
    "VAGUE_INTENT": VAGUE_INTENT_PHRASES,
    "FRIEND_ZONE": FRIEND_ZONE_PHRASES,
    "DEFLECTION": DEFLECTION_PHRASES,
    "BLAME_SHIFTING": BLAME_SHIFTING_PHRASES,
    "LACK_OF_ACCOUNTABILITY": LACK_OF_ACCOUNTABILITY_PHRASES,
    "EMOTIONAL_UNAVAILABILITY": EMOTIONAL_UNAVAILABILITY_PHRASES,
    "INCONSISTENCY": INCONSISTENCY_PHRASES,
    "GASLIGHTING": GASLIGHTING_PHRASES,
    "CONTROL_OR_DISMISSAL": CONTROL_OR_DISMISSAL_PHRASES,
}

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text

def split_messages(conversation_text):
    lines = conversation_text.splitlines()
    them_messages = []

    for line in lines:
        if ":" in line:
            speaker, message = line.split(":", 1)
            if speaker.strip().lower() in {"them", "other", "they"}:
                them_messages.append(message.strip())

    return them_messages

def detect_phrase_categories(message):
    normalized = normalize(message)
    categories = []

    for category, phrases in PHRASE_BANKS.items():
        for phrase in phrases:
            if phrase in normalized:
                categories.append(category)
                break

    return categories

def is_low_effort(message):
    words = message.split()
    return len(words) <= SHORT_REPLY_WORD_LIMIT

def has_question(message):
    return "?" in message

def analyze(conversation_text):
    them_messages = split_messages(conversation_text)

    total_messages = len(them_messages)
    flagged_messages = []
    category_counts = Counter()
    example_phrases = defaultdict(list)

    for idx, message in enumerate(them_messages):
        categories = detect_phrase_categories(message)

        if is_low_effort(message):
            categories.append("LOW_EFFORT")

        if not has_question(message):
            categories.append("NO_QUESTIONS")

        if categories:
            flagged_messages.append({
                "index": idx,
                "text": message,
                "categories": list(set(categories))
            })

            for cat in set(categories):
                category_counts[cat] += 1
                if len(example_phrases[cat]) < 3:
                    example_phrases[cat].append(message)

    flagged_count = len(flagged_messages)
    red_flag_ratio = flagged_count / total_messages if total_messages else 0

    # Escalation detection
    recent = flagged_messages[-RECENT_MESSAGE_COUNT:]
    escalation_ratio = (
        len(recent) / RECENT_MESSAGE_COUNT
        if RECENT_MESSAGE_COUNT and total_messages >= RECENT_MESSAGE_COUNT
        else 0
    )

    # Weighted severity score
    weighted_score = 0
    for category, count in category_counts.items():
        weighted_score += CATEGORY_WEIGHTS.get(category, 1) * count

    # Severity decision
    if (
        red_flag_ratio >= RED_FLAG_RATIO_LEAVE
        or "GASLIGHTING" in category_counts
        or escalation_ratio >= ESCALATION_THRESHOLD
    ):
        severity = "LEAVE"
    elif red_flag_ratio >= RED_FLAG_RATIO_CAUTION:
        severity = "CAUTION"
    else:
        severity = "CONTINUE"

    return {
        "total_messages": total_messages,
        "flagged_messages": flagged_count,
        "red_flag_ratio": round(red_flag_ratio, 2),
        "category_counts": dict(category_counts),
        "flags": dict(example_phrases),
        "severity": severity,
    }
