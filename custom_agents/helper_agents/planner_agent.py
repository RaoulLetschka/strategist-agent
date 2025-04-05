from pydantic import BaseModel

from agents import Agent

PROMPT = (
    "You are a company analysis research planner. Given a request for SWOT analysis, "
    "generate targeted web search queries to gather comprehensive information on the company's "
    "strengths, weaknesses, opportunities, and threats. Focus specifically on recent company news, "
    "earnings reports (e.g., 10-K, quarterly earnings, investor presentations), analyst insights, "
    "customer sentiment, competitive landscape, market trends, regulatory developments, and potential disruptions. "
    "Provide between 5 and 15 detailed and relevant search queries, each clearly justified."
)


class WebSearchItem(BaseModel):
    reason: str
    "Detailed explanation for why this search query is relevant and important to the SWOT analysis."

    query: str
    "The specific and targeted search term to use."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A curated list of specific web searches necessary to comprehensively perform the SWOT analysis."""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=PROMPT,
    model='gpt-4o-mini-2024-07-18',
    output_type=WebSearchPlan,
)
