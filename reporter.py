from datetime import datetime
from metrics import (
    engagement_duration,
    conversation_turns,
    extraction_completeness
)
from logger_config import get_logger

logger = get_logger()

def build_final_report(conversation, intel_store, start_time):
    end_time = datetime.now()

    metrics = {
        "engagement_duration": engagement_duration(start_time, end_time),
        "conversation_turns": conversation_turns(conversation),
        "extraction_completeness": extraction_completeness(intel_store)
    }

    logger.info("Metrics computed")
    logger.info(f"Metrics summary: {metrics}")

    final_output = {
        "metrics": metrics,
        "extracted_intelligence": intel_store,
        "session": {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }
    }

    return final_output
