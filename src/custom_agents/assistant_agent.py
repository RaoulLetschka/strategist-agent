# assistant_agent.py
from custom_agents.base import BaseAgent
from src.config import settings

class GPT4oAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="GPT-4o Assistant",
            instructions="You are a GPT-4o powered assistant.",
            deployment=settings.gpt4o_deployment,
        )

class GPT4oMiniAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="GPT-4o Mini Assistant",
            instructions="You are an efficient and fast GPT-4o-mini assistant.",
            deployment=settings.gpt4o_mini_deployment,
        )