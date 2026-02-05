from datetime import datetime, timezone
from agent.agent_loop import run_agent

from mem1.intelligence_store import (
    update_intelligence,
    build_extracted_intelligence
)

# Local runner state (Member-2)
state = {
    "history": [],               # list of {"role": "...", "content": "...", "ts": "..."}
    "sentiment_history": [],
    "current_sentiment": "friendly",
    "turn_count": 0
}

conv_id = "conv_local_001"

# Incoming scammer message
msg = "Pay to fraudster@ybl now. Use link http://fakebank.in and call 9876543210"

ts_in = datetime.now(timezone.utc).isoformat()

# ✅ Member-3 updates store with scammer message
update_intelligence(conv_id, msg, source="scammer", ts=ts_in)

# ✅ Run agent (agent_loop will update history itself)
result = run_agent(state, msg)

# If the agent returns a dict result (recommended)
reply = result.get("reply", "")
status = result.get("status", "CONTINUE")

ts_out = datetime.now(timezone.utc).isoformat()

# ✅ Member-3 updates store with agent reply (if any)
if reply:
    update_intelligence(conv_id, reply, source="agent", ts=ts_out)

# Build extracted intelligence payload (for API response)
intel = build_extracted_intelligence(conv_id)

print("Status:", status)
print("Agent reply:", reply)

print("\n--- Extracted Intelligence (for HoneypotResponse) ---")
print(intel)

print("\n--- State history ---")
for m in state["history"]:
    print(f"[{m['ts']}] {m['role']}: {m['content']}")
