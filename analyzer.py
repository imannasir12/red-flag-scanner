from rules import (
    SHORT_REPLY_WORD_LIMIT,
    RECENT_MESSAGE_COUNT,
    VAGUE_INTENT_PHRASES,
    FRIEND_ZONE_PHRASES,
    DEFLECTION_PHRASES,
    BLAME_SHIFTING_PHRASES,
    LACK_OF_ACCOUNTABILITY_PHRASES,
    EMOTIONAL_UNAVAILABILITY_PHRASES,
    INCONSISTENCY_PHRASES,
    GASLIGHTING_PHRASES,
    CONTROL_OR_DISMISSAL_PHRASES
)

def normalize(text):
    return text.lower().strip()

def detect_phrases(text, phrases):
    hits = []
    text = normalize(text)
    for phrase in phrases:
        if phrase in text:
            hits.append(phrase)
    return hits

def extract_messages(conversation_text):
    lines = conversation_text.strip().split("\n")
    messages = []
    for line in lines:
        if ":" in line:
            speaker, msg = line.split(":", 1)
            messages.append((speaker.strip(), msg.strip()))
    return messages

def detect_short_replies(messages):
    recent = messages[-RECENT_MESSAGE_COUNT:]
    their_msgs = [m for s, m in recent if s.lower() != "me"]

    if not their_msgs:
        return False

    short_count = sum(
        1 for msg in their_msgs
        if len(msg.split()) <= SHORT_REPLY_WORD_LIMIT
    )

    return short_count >= max(1, len(their_msgs) // 2)

def detect_no_questions(messages):
    recent = messages[-RECENT_MESSAGE_COUNT:]
    their_msgs = [m for s, m in recent if s.lower() != "me"]
    return all("?" not in msg for msg in their_msgs)

def analyze(conversation_text):
    messages = extract_messages(conversation_text)
    full_text = normalize(conversation_text)

    flags = {}

    phrase_checks = {
        "VAGUE_INTENT": VAGUE_INTENT_PHRASES,
        "FRIEND_ZONE": FRIEND_ZONE_PHRASES,
        "DEFLECTION": DEFLECTION_PHRASES,
        "BLAME_SHIFTING": BLAME_SHIFTING_PHRASES,
        "LACK_OF_ACCOUNTABILITY": LACK_OF_ACCOUNTABILITY_PHRASES,
        "EMOTIONAL_UNAVAILABILITY": EMOTIONAL_UNAVAILABILITY_PHRASES,
        "INCONSISTENCY": INCONSISTENCY_PHRASES,
        "GASLIGHTING": GASLIGHTING_PHRASES,
        "CONTROL_OR_DISMISSAL": CONTROL_OR_DISMISSAL_PHRASES
    }

    for category, phrases in phrase_checks.items():
        hits = detect_phrases(full_text, phrases)
        if hits:
            flags[category] = hits

    if detect_short_replies(messages):
        flags["LOW_EFFORT"] = True

    if detect_no_questions(messages):
        flags["NO_QUESTIONS"] = True

    flag_count = len(flags)

    if flag_count >= 3:
        severity = "LEAVE"
    elif flag_count == 2:
        severity = "CAUTION"
    else:
        severity = "CONTINUE"

    return {
        "flags": flags,
        "flag_count": flag_count,
        "severity": severity
    }
