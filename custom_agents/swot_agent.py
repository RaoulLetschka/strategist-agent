from pydantic import BaseModel
from typing import Literal, Tuple

from agents import Agent, function_tool

class SWOTAnalysisResult(BaseModel):
    strengths: str
    weaknesses: str
    opportunities: str
    threats: str
    summary: str

