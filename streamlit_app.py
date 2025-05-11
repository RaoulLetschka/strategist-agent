import os
import asyncio
import streamlit as st
from agents import (
    Runner, 
    set_default_openai_key, 
    set_tracing_export_api_key, 
    gen_trace_id, 
    trace,
    ModelSettings
)
from openai.types.responses import ResponseTextDeltaEvent

from custom_agents.competitors_agent import CompetitorsAgent
from custom_agents.base_agent import BaseAgent
from custom_agents.planner_agent import PlannerAgent
from custom_agents.search_agent import SearchAgent
from custom_agents.tenk_planner_agent import TenKPlannerAgent
from custom_agents.tenk_agent import TenkAgent
from custom_agents.swot_agent import SWOTAgent
from custom_agents.config import settings

set_default_openai_key(settings.openai_api_key)
set_tracing_export_api_key(settings.openai_api_key)

def initiate_default_session_state():
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = original_system_prompt

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if 'selected_agent' not in st.session_state:
        st.session_state.selected_agent = 0

    if 'temperature' not in st.session_state:
        st.session_state.temperature = 0.5
    
    if 'top_p' not in st.session_state:
        st.session_state.top_p = 1.0

    if 'max_tokens' not in st.session_state:
        st.session_state.max_tokens = 1000

    if 'tool_choice' not in st.session_state:
        st.session_state.tool_choice = "auto"

agent_options = [
    "Chatbot Agent",
    "Competitors Agent",
    "SWOT Agent",
    # "Financial Research Agent",
]

model_options = {
    "gpt-4o-mini": settings.gpt4o_mini_deployment,
    "gpt-4o": settings.gpt4o_deployment,
    "o3-mini": settings.o3_mini_deployment,
}

async def stream_results(result, message_placeholder):
    answer = ""
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            answer += event.data.delta
            message_placeholder.markdown(answer, unsafe_allow_html=True)
    return answer

async def stream_chat_message(result):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("...")
        return await stream_results(result, message_placeholder)


def main_app_sidebar():
    st.sidebar.title("Choose Agent")
    st.session_state.selected_agent = st.sidebar.radio(
        "Select an agent",
        options=agent_options,
        index=agent_options.index("Chatbot Agent"),
    )

    if st.session_state.selected_agent == "Competitors Agent":
        st.sidebar.title("Change System Prompt")
        if st.sidebar.button("Reset System Prompt"):
            st.session_state.system_prompt = original_system_prompt
        st.session_state.user_prompt = st.sidebar.text_area(
            "System Prompt", 
            value=st.session_state.system_prompt, 
            height=200, 
            key="system_prompt"
        )
        st.session_state.tool_choice = st.sidebar.selectbox(
            "Tool Choice",
            options=["auto", "required", "none"],
        )

    if st.session_state.selected_agent == "Chatbot Agent":
        st.sidebar.title("Choose Model")
        st.session_state.model = st.sidebar.radio(
            "Select a model",
            options=model_options
        )
        if st.session_state.model != "o3-mini":
            st.session_state.temperature = st.sidebar.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.1,
                format="%.1f",
            )

            st.session_state.top_p = st.sidebar.slider(
                "Top P",
                min_value=0.0,
                max_value=1.0,
                value=1.0,
                step=0.1,
                format="%.1f",
            )

            st.session_state.max_tokens = st.sidebar.number_input(
                "Max Tokens",
                min_value=500,
                max_value=5000,
                value=1000,
            )


original_system_prompt_OLD = """You are an expert strategist for a company. 
You are tasked with determining the competitors for the company based on its sector or industry.
The company has provided you with the name of the company or the Yahoo Finance ticker symbol of the company. 
Your goal is to make a SWOT analysis for each competitor.
"""

original_system_prompt = """Role: You are an expert business strategist conducting a competitor analysis.

Objective: Use the SWOT (Strengths, Weaknesses, Opportunities, Threats) framework to analyze the top competitors of a given company.

Inputs:
- Company name: {{company_name}}  

Instructions:
1. Identify if the user means by industry or by sector. If the user didn't provide that ask for that first.
2. Identify 3–5 top competitors in the same industry as {{company_name}}, using market cap, business model, or product/service overlap as criteria.
3. For each competitor, provide a concise SWOT analysis with 2–3 points per quadrant.
4. Present the findings in a structured format, labeling each competitor clearly.

Output Format:
- Competitor 1: {{name}}
  - Strengths:
  - Weaknesses:
  - Opportunities:
  - Threats:
- (Repeat for each competitor)
"""


async def app():
    initiate_default_session_state()

    main_app_sidebar()

    col1, col2 = st.columns([0.8, 0.2], vertical_alignment="bottom")
    with col1:
        st.title("Strategist Agent")
    with col2:
        st.button("Clear Chat", on_click=lambda: st.session_state.update(messages=[]))

    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if user_query := st.chat_input("Ask a question"):
        st.chat_message("user").markdown(user_query)

        st.session_state.messages.append({"role": "user", "content": user_query})
        answer = "THIS SHOULD NOT BE SEEN"

        trace_id = gen_trace_id()
        
        if st.session_state.selected_agent == "Competitors Agent":
            with trace("Competitors Agent Trace", trace_id=trace_id):
                competitors_agent = CompetitorsAgent(
                    model_settings=ModelSettings(
                        tool_choice=st.session_state.tool_choice,
                    )
                ).agent

                competitors_agent.instructions = st.session_state.system_prompt
                competitors_agent_result = Runner.run_streamed(competitors_agent, st.session_state.messages)
                competitors_agent_answer = await stream_chat_message(competitors_agent_result)
                st.session_state.messages.append({"role": "assistant", "content": competitors_agent_answer})

        elif st.session_state.selected_agent == "SWOT Agent":
            with trace("SWOT Agent Trace", trace_id=trace_id):
                # Web Planner Agent
                planner_agent = PlannerAgent()
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("...")
                    planner_result = await planner_agent.execute(f"Query: {user_query}")
                    n = 1
                    planner_answer = "### Web Search Planner Agent's Result:\n"
                    for item in planner_result.final_output.searches:
                        planner_answer += f"{n}. **Search Query:** {item.query}   \n   **Reason:** {item.reason}\n"
                        n += 1
                    message_placeholder.markdown(planner_answer, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": planner_answer})

                # Search Agent
                search_agent = SearchAgent()
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("...")
                    search_result = await search_agent.perform_search(planner_result)
                    search_answer = "## Web Search Agent's Result:\n"
                    for search in search_result:
                        search_answer += search
                    message_placeholder.markdown(search_answer, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": search_answer})

                tenk_agent = TenkAgent()
                # for search in search_queries:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("...")
                    tenk_result = await tenk_agent.execute(f"Query: {user_query}", max_turns=20)
                    tenk_search_answer = "## 10k-Filing Agent's Result:\n" + tenk_result.final_output
                    message_placeholder.markdown(tenk_search_answer, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": tenk_result})

                # SWOT Agent
                swot_agent = SWOTAgent()
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("...")
                    swot_result = await swot_agent.perform_swot_analysis(
                        user_query, 
                        str(search_result), 
                        tenk_result
                    )
                    swot_answer = (
                        "## SWOT Agent's Result:  \n  "
                        f"### SWOT Summary:\n   {swot_result.final_output.swot_summary}   \n   "
                        f"### Strenghts:\n   {swot_result.final_output.strengths}   \n   "
                        f"### Weaknesses:\n   {swot_result.final_output.weaknesses}   \n   "
                        f"### Opportunities:\n   {swot_result.final_output.opportunities}   \n   "
                        f"### Threats:\n   {swot_result.final_output.threats}   \n   "
                        f"### Web Search Summary:\n   {swot_result.final_output.summary_web_search}   \n   "
                        f"### 10k Filing Search Summary:\n   {swot_result.final_output.summary_10k_search}   \n   "
                    )
                    message_placeholder.markdown(swot_answer)
                st.session_state.messages.append({"role": "assistant", "content": swot_answer})
        else:
            with trace("Chatbot Agent Trace", trace_id=trace_id):
                # Chatbot Agent
                if st.session_state.model == "o3-mini":
                    model_settings = ModelSettings()
                else:
                    model_settings = ModelSettings(
                        temperature=st.session_state.temperature,
                        top_p=st.session_state.top_p,
                        max_tokens=st.session_state.max_tokens,
                    )
                chosen_agent = BaseAgent(
                    name="Chatbot Agent",
                    deployment=model_options[st.session_state.model],
                    model_settings=model_settings,
                )
                result = chosen_agent.execute_streamed(st.session_state.messages)
                answer = await stream_chat_message(result)
                st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    asyncio.run(app())
