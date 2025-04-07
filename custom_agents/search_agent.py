from agents import WebSearchTool
from agents.model_settings import ModelSettings
from .base_agent import BaseAgent
from .config import settings

class SearchAgent(BaseAgent):
    INSTRUCTIONS = (
        "You are a research assistant conducting focused research for a SWOT analysis. Given a targeted "
        "search query, perform a web search and summarize key findings relevant to the query concisely. "
        "Your summary should be 2-3 brief paragraphs, less than 300 words, highlighting the most important "
        "recent news, financial results, analyst insights, market developments, customer feedback, and other "
        "relevant facts. Be succinct and precise, capturing essential points while excluding any unnecessary details or commentary."
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
            name="SearchAgent",
            instructions=self.INSTRUCTIONS,
            deployment=settings.gpt4o_mini_deployment,
            model_settings=ModelSettings(tool_choice="required"),
            tools=[WebSearchTool()],
        )