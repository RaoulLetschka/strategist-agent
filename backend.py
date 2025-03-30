import os

from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv


app = FastAPI(
    title="Competitors Agent",
    description="An agent that provides competitor analysis using the SWOT framework.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "competitors",
            "description": "Endpoints related to competitor analysis.",
        },
    ],
)

@app.get("/", tags=["competitors"])
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": f"Competitors Agent API is running. os.getenv('OPENAI_API_KEY')={os.getenv('OPENAI_API_KEY')}"}

@app.get("/competitors/{company_name}", tags=["competitors"])
async def get_competitors(company_name: str):
    """
    Endpoint to get competitors for a given company name.
    """
    # Placeholder for actual logic to fetch competitors
    # In a real application, this would involve calling the agent and processing the response.
    competitors = ["Competitor A", "Competitor B", "Competitor C"]
    return {"company": company_name, "competitors": competitors}

if __name__ == "__main__":
    _ = load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=8000)