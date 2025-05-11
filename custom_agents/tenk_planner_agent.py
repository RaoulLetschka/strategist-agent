from pydantic import BaseModel
from agents import Agent

from custom_agents.base_agent import BaseAgent
from custom_agents.config import settings

# Competitor of SAP
competitors = {
    "Apple Inc.": "AAPL",
    "Microsoft Corporation": "MSFT",
    "NVIDIA Corporation": "NVDA",
    "Broadcom Inc.": "AVGO",
    "Oracle Corporation": "ORCL",
    "Salesforce, Inc.": "CRM",
    "Cisco Systems, Inc.": "CSCO",
    "International Business Machines Corporation": "IBM",
    "Palantir Technologies Inc.": "PLTR",
    "Accenture plc": "ACN",
    "Salesforce, Inc.": "CRM",
    "Intuit Inc.": "INTU",
    "ServiceNow, Inc.": "NOW",
    "Adobe Inc.": "ADBE",
    "Uber Technologies, Inc.": "UBER",
    "Automatic Data Processing, Inc.": "ADP",
    "AppLovin Corporation": "APP",
    "Cadence Design Systems, Inc.": "CDNS",
    "MicroStrategy Incorporated": "MSTR",
    "Workday, Inc.": "WDAY",
    "SAP SE": "SAP",
}

class TenKSearchPlan(BaseModel):
    searches: list[str]
    """A curated list of specific Azure AI Search vector index searches necessary."""


class TenKPlannerAgent(BaseAgent):
    INSTRUCTIONS = (
        "You are an SEC‑10K Retrieval Planner. For every user request, think silently, then output ONLY a list "
        "of query strings—no answers, no commentary.\n\n"

        # —— Core task ——————————————————————————————————————————
        "Goal: craft search queries that pull the exact 10‑K pages an analyst would need for a rigorous, "
        "quantitative SWOT analysis of the target company.\n"

        # —— 10‑K mapping to SWOT ————————————————————————
        "• Strengths  → Business Overview, MD&A (competitive advantages, assets, IP).\n"
        "• Weaknesses → Risk Factors, MD&A (operational gaps, liabilities, legal issues).\n"
        "• Opportunities → MD&A, Strategy language, Forward‑looking statements (growth initiatives, markets).\n"
        "• Threats → Risk Factors, Competition, Legal Proceedings (external pressures, regulation, disruption).\n\n"

        # —— Query‑building rules ——————————————————————————
        "1. Each query must be a single string:  '<COMPANY NAME> <SWOT topic keywords>'.\n"
        "2. Use synonyms where helpful (e.g., 'supply‑chain risk', 'competitive moat').\n"
        "3. Create as many queries as needed to cover all four pillars—typically 6‑12 total.\n"
        "4. Order queries logically: strengths first, then weaknesses, opportunities, threats.\n\n"

        # —— Validation & error handling ————————————————————
        f"In the index `10k-filings-index` are filings only for companies in the dictionary `competitors` = {competitors}.\n"
        "If the user’s company is missing from that list, or the request is not about 10‑K filings, "
        "return exactly the string: 10k-filing not found in vector index\n"
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
            name="TenKPlannerAgent",
            instructions=self.INSTRUCTIONS,
            deployment=settings.o3_mini_deployment,
            output_type=TenKSearchPlan,
        )