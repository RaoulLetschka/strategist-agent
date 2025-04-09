from pydantic import BaseModel
from typing import Literal

from .base_agent import BaseAgent
from .config import settings

class SWOTCategoryResult(BaseModel):
    category: Literal["STRENGTHS", "WEAKNESSES", "OPPORTUNITIES", "THREATS"]
    """The category of the SWOT analysis."""
    
    analysis: str
    """The analysis for the given category."""
    
    summary: str
    """A summary of the analysis for the given category."""


def _swot_category_instructions(category: str) -> str:
    return (
        "You are a business analyst tasked with performing an analysis for a company for "
        f"the {category} of the 4 SWOT categories 'STRENGTHS', 'WEAKNESSES', 'OPPORTUNITIES', 'THREATS'. "
        "You will be provided with the company's name and input text that is the basis for you analysis. "
        "Use only the input text to perform the analysis. "
        "You should provide the analysis itself and a summary of the analysis.\n"
        "The analysis should be detailed and provide insights into the company's position in the market."
    )


class SWOTCategoryAgent(BaseAgent):
    def __init__(self, category: Literal["STRENGTHS", "WEAKNESSES", "OPPORTUNITIES", "THREATS"]):
        self.category = category
        self.INSTRUCTIONS = _swot_category_instructions(category)
        super().__init__(
            name="SWOTCategoryAgent",
            instructions=self.INSTRUCTIONS,
            deployment=settings.gpt4o_mini_deployment,
            output_type=SWOTCategoryResult,
        )