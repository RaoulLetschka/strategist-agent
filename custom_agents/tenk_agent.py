from langchain.chains import RetrievalQA
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate 

from custom_agents.config import settings
from custom_agents.search_utils.vector_search import AzureSearchRetriever

class TenkAgent:
    """
    TenkAgent is a specialized agent for analyzing 10-K filings.
    It retrieves relevant documents from an Azure Search index and uses a language model to summarize and answer questions based on the retrieved documents.
    """

    INSTRUCTIONS = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are part of a team that specializes in company analysis and research.
        You are given a search query to retrieve chunks of 10k filings, which are stored in a vector storage.
        You are tasked with providing a summary of the search results and then answering the question based on the context.
        Include financial data if available in the context. 
        Identify the company name and year from the context and state them in the answer.
        If the search query is not relevant to the context, respond with "No relevant information found.".
        You should ONLY include information that is in the context.
        ALWAYS cite the source documents in your answer.

        Context:
        {context}

        Question: {question}
        """,
    )

    def __init__(self, k: int = 5):
        self.k = k
        self.retriever = AzureSearchRetriever()
        self.retriever.k = k
        self.llm = AzureChatOpenAI(
            openai_api_version=settings.azure_openai_api_version,
            openai_api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            azure_deployment=settings.gpt4o_mini_deployment,
            temperature=0,
            max_tokens=500,
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",               # or "map_reduce", "refine", etc.
            retriever=self.retriever,
            chain_type_kwargs={"prompt": self.INSTRUCTIONS},
            return_source_documents=True,
        )

    def run(self, search_query: str):
        return self._get_answer(search_query)

    def _get_answer(self, search_query: str):
        return self.qa_chain.invoke({"query": search_query})









# result = qa_chain.invoke({"query": search_query})
# print(f"Query: {result['query']} - Result: {result['result']}")
# for doc in result["source_documents"]:
#     print(f"- {doc.metadata['company']} ({doc.metadata['year']}, {doc.metadata['tenkpage']}): {doc.page_content[:500]}…")