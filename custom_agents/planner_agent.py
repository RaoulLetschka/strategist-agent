from pydantic import BaseModel
from dotenv import load_dotenv
import os
from agents import Agent

from .base_agent import BaseAgent

_ = load_dotenv()

class WebSearchItem(BaseModel):
    reason: str
    "Detailed explanation for why this search query is relevant and important to the SWOT analysis."

    query: str
    "The specific and targeted search term to use."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A curated list of specific web searches necessary to comprehensively perform the SWOT analysis."""


class PlannerAgent(BaseAgent):
    INSTRUCTIONS = (
        "You are a company analysis research planner. Given a request for SWOT analysis, "
        "generate targeted web search queries to gather comprehensive information on the company's "
        "strengths, weaknesses, opportunities, and threats. Focus specifically on recent company news, "
        "earnings reports (e.g., 10-K, quarterly earnings, investor presentations), analyst insights, "
        "customer sentiment, competitive landscape, market trends, regulatory developments, and potential disruptions. "
        "Provide between 5 and 15 detailed and relevant search queries, each clearly justified."
    )

    def __init__(self):
        """
        Initialize the PlannerAgent with the given parameters.
        :param name: The name of the agent.
        :param instructions: Instructions for the agent.
        :param
        deployment: The deployment name for the Azure OpenAI model.
        :param output_type: The type of output expected from the agent.
        """
        super().__init__(
            name="PlannerAgent",
            instructions=self.INSTRUCTIONS,
            deployment=os.getenv("O3_MINI_DEPLOYMENT"),
            output_type=WebSearchPlan,
        )