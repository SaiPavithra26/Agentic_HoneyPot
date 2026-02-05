from datetime import datetime, timedelta
from metrics import (
    engagement_duration,
    conversation_turns,
    extraction_completeness
)

def test_engagement_duration():
    start = datetime.now()
    end = start + timedelta(seconds=30)
    assert engagement_duration(start, end) == 30

def test_conversation_turns():
    conversation = ["hi", "hello", "upi?", "abc@upi"]
    assert conversation_turns(conversation) == 4

def test_extraction_completeness():
    intel_store = {
        "upi_ids": ["abc@upi"],
        "bank_accounts": [],
        "urls": ["http://test.com"],
        "phone_numbers": []
    }
    assert extraction_completeness(intel_store) == 0.67
