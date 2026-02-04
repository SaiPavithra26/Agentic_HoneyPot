
def detect_scam(message: str) -> dict:
    """
    Lightweight scam detector (LLM-ready).
    Replace logic with LLM later.
    """
    keywords = ["blocked", "urgent", "verify", "upi", "bank", "refund", "otp"]

    score = sum(1 for k in keywords if k in message.lower())

    is_scam = score >= 2

    scam_type = None
    if "upi" in message.lower():
        scam_type = "UPI_FRAUD"
    elif "bank" in message.lower():
        scam_type = "BANK_FRAUD"
    elif "link" in message.lower():
        scam_type = "PHISHING"

    return {
        "is_scam": is_scam,
        "scam_type": scam_type,
        "confidence": min(0.6 + score * 0.1, 0.95)
    }
