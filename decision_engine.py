import re

# lightweight patterns for stop condition
UPI_RE = re.compile(r"\b[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}\b")
BANK_RE = re.compile(r"\b\d{9,18}\b")
URL_RE = re.compile(r"\bhttps?://[^\s]+\b", re.IGNORECASE)
IFSC_RE = re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b")

def map_strategy(sentiment: str) -> str:
    """
    Maps scammer sentiment to engagement strategy
    """
    if sentiment == "aggressive":
        return "calm_compliance"
    elif sentiment == "impatient":
        return "delay_verify"
    else:
        return "friendly_extract"


def should_stop(state) -> bool:
    # 1) Hard cap on turns (prevents infinite loops)
    if state.get("turn_count", 0) >= 8: return True


    # 2) Build recent conversation text (supports dict or string history)
    recent = state.get("history", [])[-8:]
    texts = [(m.get("content", "") if isinstance(m, dict) else str(m)) for m in recent]
    convo = " ".join(texts).lower()

    # 3) Stop if scammer ends conversation
    if any(x in convo for x in ["bye", "stop", "don't message", "do not message", "cancel"]):
        return True


    # 4) Stop if we have enough actionable intelligence signals in the convo itself
    # (since Member 3 does the official validated extraction elsewhere)
    upis = UPI_RE.findall(" ".join(texts))
    banks = BANK_RE.findall(" ".join(texts))
    links = URL_RE.findall(" ".join(texts))
    ifscs = IFSC_RE.findall(" ".join(texts).upper())

    # Consider it "enough" if we got 2+ different categories or 2 total strong items
    score = 0
    if upis: score += 1
    if links: score += 1
    if banks: score += 1
    if ifscs: score += 1

    if score >= 2:
        return True

    return False
