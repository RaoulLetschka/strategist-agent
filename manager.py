from __future__ import annotations

import asyncio
import time
from collections.abc import Sequence

from rich.console import Console

from agents import (
    Agent,
    Runner, 
    RunResult, 
    custom_span, 
    gen_trace_id, 
    trace
)
import streamlit as st

from custom_agents.planner_agent import WebSearchItem, WebSearchPlan, PlannerAgent
from custom_agents.search_agent import SearchAgent
# from .custom_agents.helper_agents.writer_agent import FinancialReportData, writer_agent
from custom_agents.swot_agent import SWOTAnalysisResult, SWOTAgent
from custom_agents.printer import Printer

async def _summary_extractor(run_result: RunResult) -> str:
    """Custom output extractor for sub‑agents that return an AnalysisSummary."""
    # The financial/risk analyst agents emit an AnalysisSummary with a `summary` field.
    # We want the tool call to return just that summary text so the writer can drop it inline.
    return str(run_result.final_output.summary)


class SWOTAnalysisManager:
    """
    Orchestrates the full flow: planning, searching, sub‑analysis, writing, and verification.
    """

    def __init__(self) -> None:
        self.search_agent = SearchAgent()
        self.planner_agent = PlannerAgent()
        self.swot_agent = SWOTAgent()

    async def execute_streamed(self, query: str, messages: str | None = None) -> str:
        """
        Execute the agent with the given prompt and stream the output.
        :param prompt: The prompt to execute.
        :return: An async generator that yields the streamed output.
        """
        search_plan = await self._plan_searches(query)
        print(f"Search plan: {search_plan}")
        search_results = await self._perform_searches(search_plan)
        print(f"Search results: {search_results}")
        report = await self._write_report(query, search_results)
        print(f"Report: {report}")
        return Runner.run_streamed(self.swot_agent, report)

    async def run(self, query: str) -> None:
        trace_id = gen_trace_id()
        with trace("SWOT research trace", trace_id=trace_id):
            self.printer.update_item(
                "trace_id",
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}",
                is_done=True,
                hide_checkmark=True,
            )
            self.printer.update_item("start", "Starting SWOT research...", is_done=True)
            search_plan = await self._plan_searches(query)
            search_results = await self._perform_searches(search_plan)
            report = await self._write_report(query, search_results)
            # verification = await self._verify_report(report)

            final_report = f"SWOT summary\n\n{report.swot_summary}"
            self.printer.update_item("final_report", final_report, is_done=True)

            self.printer.end()

        # Print to stdout
        print("\n\n=====REPORT=====\n\n")
        print(f"SWOT summary:\n{report.swot_summary}\n")
        print(f"Strengths:\n{report.strengths}\n")
        print(f"Weaknesses:\n{report.weaknesses}\n")
        print(f"Opportunities:\n{report.opportunities}\n")
        print(f"Threats:\n{report.threats}")
        # print("\n\n=====FOLLOW UP QUESTIONS=====\n\n")
        # print("\n".join(report.follow_up_questions))
        # print("\n\n=====VERIFICATION=====\n\n")
        # print(verification)

    async def _plan_searches(self, query: str) -> WebSearchPlan:
        result = await PlannerAgent().execute(f"Query: {query}")
        return result.final_output_as(WebSearchPlan)

    async def _perform_searches(self, search_plan: WebSearchPlan) -> Sequence[str]:
        with custom_span("Search the web"):
            tasks = [asyncio.create_task(self._search(item)) for item in search_plan.searches]
            results: list[str] = []
            num_completed = 0
            for task in asyncio.as_completed(tasks):
                result = await task
                if result is not None:
                    results.append(result)
                num_completed += 1
            return results

    async def _search(self, item: WebSearchItem) -> str | None:
        input_data = f"Search term: {item.query}\nReason: {item.reason}"
        try:
            result = await SearchAgent().execute(input_data)
            return str(result.final_output)
        except Exception:
            return None

    async def _write_report(self, query: str, search_results: Sequence[str]) -> SWOTAnalysisResult:
        input_data = f"Original query: {query}\nSummarized search results: {search_results}"
        result = Runner.run_streamed(SWOTAgent().agent, input_data)
        return result.final_output_as(SWOTAnalysisResult)

    # async def _verify_report(self, report: FinancialReportData) -> VerificationResult:
    #     self.printer.update_item("verifying", "Verifying report...")
    #     result = await Runner.run(verifier_agent, report.markdown_report)
    #     self.printer.mark_item_done("verifying")
    #     return result.final_output_as(VerificationResult)
