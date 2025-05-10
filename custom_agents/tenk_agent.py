import os
from typing import List, Dict, Any

from pydantic import BaseModel
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from agents import (
    function_tool,
    ModelSettings
)

from custom_agents.config import settings
from custom_agents.base_agent import BaseAgent
from custom_agents.tenk_planner_agent import TenKPlannerAgent



credential = AzureKeyCredential(settings.azure_search_api_key)
search_client = SearchClient(
    endpoint=settings.azure_search_service_endpoint,
    index_name=settings.azure_search_index_name,
    credential=credential
)

class DocumentChunk(BaseModel):
    """
    A single chunk of a 10-K filing, with metadata for citation.
    """
    data: str
    company: str
    year: int
    tenkpage: int
    metadata: str

@function_tool
def retrieve_tenk_chunks(query: str, k: int = 3) -> List[DocumentChunk]:
    """
    Retrieve the top k chunks from the Azure Search 10-K index for a given query.
    """
    results = search_client.search(search_text=query, top=k)
    chunks: List[DocumentChunk] = []
    for r in results:
        chunks.append(
            DocumentChunk(
                data=r["data"],
                company=r["companyname"],
                year=r["year"],
                tenkpage=r["tenkpage"],
                metadata=r["metadata"],
            )
        )
    return chunks


class TenkAgent(BaseAgent):
    """
    An agent that plans, retrieves and summarizes 10-K filings using Azure Search.
    """

    INSTRUCTIONS = """
    You are part of a team that specializes in company analysis and research.
    You have access to two tools. The `tenk_planner_tool`, which plans the search queries for 10-k filings "
    "in a vector storage and the `retrieve_tenk_chunks(query, k)`, which returns relevant chunks of 10-K filings from the search queries.
    Your task:
    1. Use the `tenk_planner_tool` to plan the search queries for 10-K filings.
    2. If the `tenk_planner_tool` gives you usable search queries, use the `retrieve_tenk_chunks(query, k)` to retrieve relevant chunks of 10-K filings based on the planned queries.
    3. Call `retrieve_tenk_chunks` with the search queries to get context.
    4. Summarize the search results in {max_token}.
    5. Answer the user’s question using ONLY that context.
    6. Include any financial data present.
    7. Identify the company name and year, and state them.
    8. ALWAYS cite the source documents in your answer.
    If no relevant information is found, respond with “No relevant 10-k filing information found.” 
    """

    def __init__(self, k: int = 5, max_token: int = 1000):
        self.k = k
        self.max_token = max_token
        super().__init__(
            name="TenkAgent",
            instructions=self.INSTRUCTIONS.format(max_token=max_token),
            deployment=settings.gpt4o_mini_deployment,
            model_settings=ModelSettings(temperature=0, max_tokens=max_token),
            tools=[
                TenKPlannerAgent().agent.as_tool(
                    tool_name="tenk_planner_tool",
                    tool_description="Plans the search queries for 10-K filings."
                ),
                retrieve_tenk_chunks,
            ]
        )
