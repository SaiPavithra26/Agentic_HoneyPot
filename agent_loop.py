from agent.reply_generator import generate_agent_reply
from agent.intelligence_extractor import extract_intelligence
from agent.decision_engine import should_stop

def run_agent(state, scammer_message):
    # 1) update history
    state["history"].append(f"Scammer: {scammer_message}")
    state["turn_count"] = state.get("turn_count", 0) + 1

    # 2) extract intelligence
    state["extracted_intelligence"] = extract_intelligence(state["history"])

    # 3) stop check
    if should_stop(state):
        return {
            "status": "COMPLETED",
            "intelligence": state["extracted_intelligence"],
            "turns": state["turn_count"]
        }

    # 4) generate reply
    reply = generate_agent_reply(state)
    state["history"].append(f"User: {reply}")

    return {
        "status": "CONTINUE",
        "reply": reply,
        "turn": state["turn_count"]
    }
