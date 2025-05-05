from pydantic import BaseModel
from typing import Literal, Tuple

from agents import Agent, function_tool, OpenAIChatCompletionsModel
import yfinance as yf
from yfinance.const import SECTOR_INDUSTY_MAPPING, EQUITY_SCREENER_FIELDS
from .models.azure_openai_client import AzureOpenAIClient
from .config import settings


class SectorIndustryMapping(BaseModel):
    sector: str
    industry: str

    class Config:
        extra = "forbid"

class TickerNameMapping(BaseModel):
    ticker: str
    name: str

    class Config:
        extra = "forbid"

@function_tool()
def determine_competitors(company_ticker: str, sector_or_industry: Literal["sectorKey", "industryKey"]) -> Tuple[dict, dict]:
    """
    Determine the top competitors of a given company based on its sector or industry.
    Args:
        company_ticker (str): The stock ticker symbol of the company.
        sector_or_industry (Literal["sectorKey", "industryKey"]): Specify whether to determine competitors based on the company's sector or industry.
    Returns:
        list: A list of top competitor companies.
    Raises:
        KeyError: If the specified sector_or_industry is not found in the company's information.
        ValueError: If the company ticker is invalid or not found.
    """
    company = yf.Ticker(company_ticker)
    
    view = yf.Sector(company.info[sector_or_industry]) if sector_or_industry == "sectorKey" else yf.Industry(company.info[sector_or_industry])
    competitors = view.top_companies.drop(columns='rating').reset_index().to_dict('records')
    overview = view.overview

    return competitors, overview

get_ticker_agent = Agent(
    name="Get ticker of a company",
    instructions=(
        "You are an expert assistant whose sole task is to provide the correct "
        "Yahoo Finance ticker symbol and name for a given company."
    ),
    model='gpt-4o-mini-2024-07-18',
    output_type=TickerNameMapping,
)

def dynamic_instructions(system_prompt: str) -> str:
    return system_prompt

class CompetitorsAgent():
    """
    CompetitorsAgent is an agent that determines the top competitors of a given company based on its sector or industry.
    It uses the yfinance library to fetch the company's information and the competitors' data.
    """

    def __init__(self, **kwargs):
        self.agent = Agent(
            name="Competitors Agent",
            instructions=dynamic_instructions,
            model=OpenAIChatCompletionsModel(
                model=settings.gpt4o_mini_deployment,
                openai_client=AzureOpenAIClient.create_async_client(settings.gpt4o_mini_deployment),
            ),
            tools=[
                get_ticker_agent.as_tool(
                    tool_name="get_ticker",
                    tool_description="Get ticker and name of a company"
                ),
                determine_competitors,
            ],
            **kwargs
        )
