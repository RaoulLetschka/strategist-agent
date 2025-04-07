from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings

INSTRUCTIONS = (
    "You are a research assistant conducting focused research for a SWOT analysis. Given a targeted "
    "search query, perform a web search and summarize key findings relevant to the query concisely. "
    "Your summary should be 2-3 brief paragraphs, less than 300 words, highlighting the most important "
    "recent news, financial results, analyst insights, market developments, customer feedback, and other "
    "relevant facts. Be succinct and precise, capturing essential points while excluding any unnecessary details or commentary."
)

search_agent = Agent(
    name="SearchAgent",
    instructions=INSTRUCTIONS,
    model='gpt-4o-mini-2024-07-18',
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
)
