from pydantic import BaseModel
from typing import Literal

from agents import Agent

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

swot_strengths_agent = Agent(
    name="SWOT strengths Agent",
    instructions=_swot_category_instructions("STRENGTHS"),
    model='gpt-4o-mini-2024-07-18',
    output_type=SWOTCategoryResult,
)

swot_weaknesses_agent = Agent(
    name="SWOT weaknesses Agent",
    instructions=_swot_category_instructions("WEAKNESSES"),
    model='gpt-4o-mini-2024-07-18',
    output_type=SWOTCategoryResult,
)

swot_opportunities_agent = Agent(
    name="SWOT opportunities Agent",
    instructions=_swot_category_instructions("OPPORTUNITIES"),
    model='gpt-4o-mini-2024-07-18',
    output_type=SWOTCategoryResult,
)

swot_threats_agent = Agent(
    name="SWOT threats Agent",
    instructions=_swot_category_instructions("THREATS"),
    model='gpt-4o-mini-2024-07-18',
    output_type=SWOTCategoryResult,
)