# mem1/intelligence_store.py
import re
from typing import Dict, Set, List, Any
from urllib.parse import urlparse

# ---------- Patterns ----------
UPI_RE = re.compile(r"\b[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}\b")
BANK_RE = re.compile(r"\b\d{9,18}\b")
URL_RE = re.compile(r"\bhttps?://[^\s]+\b", re.IGNORECASE)
PHONE_RE = re.compile(r"\b[6-9]\d{9}\b")

# ---------- In-memory store ----------
_STORE: Dict[str, Dict[str, Set[str]]] = {}

# ---------- Validators ----------
def valid_upi(u):
    return "@" in u and len(u) < 50

def valid_bank(a):
    return a.isdigit() and 9 <= len(a) <= 18

def valid_url(u):
    p = urlparse(u)
    return p.scheme in ("http", "https") and bool(p.netloc)

# ---------- Core Functions ----------

def update_intelligence(conversation_id: str, text: str, source: str, ts: str):
    """Extract + validate + dedupe"""
    if conversation_id not in _STORE:
        _STORE[conversation_id] = {
            "upi_ids": set(),
            "bank_accounts": set(),
            "phishing_links": set(),
            "phone_numbers": set()
        }

    rec = _STORE[conversation_id]

    # UPI
    for u in UPI_RE.findall(text or ""):
        u = u.lower()
        if valid_upi(u):
            rec["upi_ids"].add(u)

    # Bank
    for b in BANK_RE.findall(text or ""):
        if valid_bank(b):
            rec["bank_accounts"].add(b)

    # URL
    for l in URL_RE.findall(text or ""):
        if valid_url(l):
            rec["phishing_links"].add(l)

    # Phone
    for p in PHONE_RE.findall(text or ""):
        rec["phone_numbers"].add(p)

    return rec


def build_extracted_intelligence(conversation_id: str) -> Dict[str, Any]:
    """Return data in API-model shape"""
    rec = _STORE.get(conversation_id)

    if not rec:
        return {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_links": [],
            "phone_numbers": [],
            "other_intelligence": {}
        }

    return {
        "bank_accounts": list(rec["bank_accounts"]),
        "upi_ids": list(rec["upi_ids"]),
        "phishing_links": list(rec["phishing_links"]),
        "phone_numbers": list(rec["phone_numbers"]),
        "other_intelligence": {}
    }
