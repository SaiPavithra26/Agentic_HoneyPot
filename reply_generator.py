from agent.llm_client import BedrockLLM
from agent.decision_engine import map_strategy

llm = BedrockLLM(model="llama3")

def generate_agent_reply(state):

    conversation = "\n".join(state["history"])
    sentiment = state.get("current_sentiment", "friendly")
    strategy = map_strategy(sentiment)

    prompt = f"""
You are acting as a real human user who believes the other person is genuine support.

Current engagement strategy: {strategy}

Strategy guide:
- calm_compliance → show fear and ask how to pay / which bank
- delay_verify → ask for clarification and more time
- friendly_extract → politely ask for account or UPI details

Rules (STRICT):
1. Sound natural and human
2. Ask ONLY ONE question
3. Maximum 2 lines
4. NO emojis
5. Never say the word scam or accuse
6. Do not be overly formal

Conversation so far:
{conversation}

Generate ONLY the reply text:
"""

    reply = llm.ask(prompt)

    # safety cleanup
    reply = reply.replace("😟", "").replace("😰", "").strip()

    return reply
