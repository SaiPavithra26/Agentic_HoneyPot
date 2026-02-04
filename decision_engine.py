def map_strategy(sentiment):
    """
    Maps scammer sentiment to engagement strategy
    """
    if sentiment == "aggressive":
        return "calm_compliance"
    elif sentiment == "impatient":
        return "delay_verify"
    else:
        return "friendly_extract"


def should_stop(state):
    intel = state.get("extracted_intelligence", {})

    # Stop if any high-value intel is captured
    return any([
        intel.get("bank_accounts"),
        intel.get("upi_ids"),
        intel.get("phishing_links")
    ])
