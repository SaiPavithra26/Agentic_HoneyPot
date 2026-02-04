
from agent.strategy import STRATEGY_MAP
from agent.persona import BASE_PERSONA, PANICKED_PERSONA

def build_prompt(state: dict, scammer_message: str) -> str:
    strategy = STRATEGY_MAP[state["current_sentiment"]]

    persona = BASE_PERSONA
    if state["current_sentiment"] == "aggressive":
        persona = PANICKED_PERSONA

    history = "\n".join(state["history"])

    return f"""
{persona}

Current tone: {strategy['tone']}
Objective: {strategy['goal']}

Conversation history:
{history}

Scammer says:
"{scammer_message}"

Reply naturally like a human.
Do not expose detection.
"""
