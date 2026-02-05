from datetime import datetime

def engagement_duration(start_time, end_time):
    return int((end_time - start_time).total_seconds())

def conversation_turns(conversation):
    return len(conversation)

def extraction_completeness(intel_store):
    required_fields = ["upi_ids", "bank_accounts", "urls"]
    found = 0

    for field in required_fields:
        if intel_store.get(field):
            found += 1

    return round(found / len(required_fields), 2)
