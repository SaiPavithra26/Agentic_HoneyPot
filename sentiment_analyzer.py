
def detect_sentiment(message: str) -> str:
    """
    Classifies scammer sentiment.
    """

    msg = message.lower()

    aggressive = ["blocked", "legal", "final warning", "account frozen"]
    impatient = ["urgent", "immediately", "now", "fast"]

    if any(word in msg for word in aggressive):
        return "aggressive"

    if any(word in msg for word in impatient):
        return "impatient"

    return "friendly"
