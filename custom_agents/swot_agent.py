import os 
from pydantic import BaseModel
from typing import Literal, Tuple

from agents import Agent, function_tool, ModelSettings
from .base_agent import BaseAgent
from .swot_category_agents import SWOTCategoryAgent


class SWOTAnalysisResult(BaseModel):
    strengths: str
    """The strengths of the company."""

    weaknesses: str
    """The weaknesses of the company."""

    opportunities: str
    """The opportunities available to the company."""

    threats: str
    """The threats to the company."""

    swot_summary: str
    """A summary of the SWOT analysis."""

INSTRUCTIONS = (
    "You are a business analyst tasked with performing a comprehensive SWOT analysis for a company. "
    "You have access to four specialized sub-agents that provide detailed analyses of the company’s strengths, weaknesses, opportunities, and threats respectively. "
    "Your task is to:"
	"1.	Query each sub-agent for their respective analysis strictly based on the company’s available data."
	"2.	Collect and integrate the outputs from all four sub-agents."
	"3.	Synthesize a coherent and comprehensive SWOT analysis using only the information provided by the sub-agents."
	"4.	Present your final output with clearly labeled sections: Strengths, Weaknesses, Opportunities, Threats, and a Summary that encapsulates the overall analysis."
	"5.	Do not include any external or additional information beyond what is supplied by the sub-agents."
)

class SWOTAgent(BaseAgent):
    INSTRUCTIONS = (
        "You are a business analyst tasked with performing a comprehensive SWOT analysis for a company. "
        "You have access to four specialized sub-agents that provide detailed analyses of the company’s strengths, weaknesses, opportunities, and threats respectively. "
        "Your task is to:"
        "1.	Query each sub-agent for their respective analysis strictly based on the company’s available data."
        "2.	Collect and integrate the outputs from all four sub-agents."
        "3.	Synthesize a coherent and comprehensive SWOT analysis using only the information provided by the sub-agents."
        "4.	Present your final output with clearly labeled sections: Strengths, Weaknesses, Opportunities, Threats, and a Summary that encapsulates the overall analysis."
        "5.	Do not include any external or additional information beyond what is supplied by the sub-agents."
    )

    def __init__(self):
        super().__init__(
            name="SWOTAgent",
            instructions=self.INSTRUCTIONS,
            deployment=os.getenv("GPT4O_MINI_DEPLOYMENT"),
            tools=[
                SWOTCategoryAgent("STRENGTHS").agent.as_tool(
                    tool_name="strengths_analysis_tool",
                    tool_description="Analyzes and identifies the strengths of the company based on the provided data."
                ),
                SWOTCategoryAgent("WEAKNESSES").agent.as_tool(
                    tool_name="weaknesses_analysis_tool",
                    tool_description="Evaluates and highlights the weaknesses of the company using the given information."
                ),
                SWOTCategoryAgent("OPPORTUNITIES").agent.as_tool(
                    tool_name="opportunities_analysis_tool",
                    tool_description="Explores and identifies potential opportunities available to the company."
                ),
                SWOTCategoryAgent("THREATS").agent.as_tool(
                    tool_name="threats_analysis_tool",
                    tool_description="Assesses and identifies potential threats to the company from the provided data."
                ),
            ],
            output_type=SWOTAnalysisResult,
            model_settings=ModelSettings(tool_choice="required")
        )