import os
import asyncio
import streamlit as st
from agents import Runner, set_default_openai_key, set_tracing_export_api_key, gen_trace_id, trace
from openai.types.responses import ResponseTextDeltaEvent
from custom_agents.competitors_agent import competitors_agent
from manager import SWOTAnalysisManager

from custom_agents.base_agent import BaseAgent
from custom_agents.planner_agent import WebSearchPlan
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

    if st.session_state.selected_agent == "Chatbot Agent":
        st.sidebar.title("Choose Model")
        st.session_state.model = st.sidebar.radio(
            "Select a model",
            options=model_options
        )

        # TODO: Decide if we want to keep this
        # st.session_state.temperature = st.sidebar.slider(
        #     "Temperature",
        #     min_value=0.0,
        #     max_value=1.0,
        #     value=0.5,
        #     step=0.1,
        #     format="%.1f",
        # )

original_system_prompt = """You are an expert strategist for a company. 
You are tasked with determining the top competitors for the company based on its sector or industry.
The company has provided you with the the name of the company or the Yahoo Finance ticker symbol of the company. 
Your goal is to make a competitor analysis with the SWOT framework.
"""

async def app():
    initiate_default_session_state()

    main_app_sidebar()

    col1, col2 = st.columns([0.8, 0.2], vertical_alignment="bottom")
    with col1:
        st.title("Strategist Agent")
    with col2:
        st.button("Clear Chat", on_click=lambda: st.session_state.update(messages=[]))

    competitors_agent.instructions = st.session_state.system_prompt
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Ask a question"):
        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})
        answer = "THIS SHOULD NOT BE SEEN"

        trace_id = gen_trace_id()
        
        if st.session_state.selected_agent == "Competitors Agent":
            with trace("Competitors Agent Trace", trace_id=trace_id):
                # TODO: refactor competitor agent to use the new agent system
                competitors_agent_result = Runner.run_streamed(competitors_agent, st.session_state.messages)
                competitors_agent_answer = await stream_chat_message(competitors_agent_result)
                st.session_state.messages.append({"role": "assistant", "content": competitors_agent_answer})

        elif st.session_state.selected_agent == "SWOT Agent":
            with trace("SWOT Agent Trace", trace_id=trace_id):
                chosen_agent = SWOTAnalysisManager()
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("...")
                    planner_result = await chosen_agent.planner_agent.execute(f"Query: {st.session_state.messages}")
                    n = 1
                    planner_answer = "### Planner Agent's Result:\n"
                    for item in planner_result.final_output.searches:
                        planner_answer += f"{n}. **Search Query:** {item.query}   \n   **Reason:** {item.reason}\n"
                        n += 1
                    message_placeholder.markdown(planner_answer, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": planner_answer})

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("...")
                    search_plan = await chosen_agent.perform_search(planner_result)
                    search_answer = "## Search Agent's Result:\n"
                    for search in search_plan:
                        search_answer += search
                    message_placeholder.markdown(search_answer, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": search_answer})

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("...")
                    swot_result = await chosen_agent.perform_swot_analysis(st.session_state.messages, str(search_plan))
                    swot_answer = (
                        "## SWOT Agent's Result:  \n  "
                        f"### SWOT Summary:\n   {swot_result.final_output.swot_summary}   \n   "
                        f"### Strenghts:\n   {swot_result.final_output.strengths}   \n   "
                        f"### Weaknesses:\n   {swot_result.final_output.weaknesses}   \n   "
                        f"### Opportunities:\n   {swot_result.final_output.opportunities}   \n   "
                        f"### Threats:\n   {swot_result.final_output.threats}   \n   "
                    )
                    message_placeholder.markdown(swot_answer)
                st.session_state.messages.append({"role": "assistant", "content": swot_answer})
        else:
            with trace("Chatbot Agent Trace", trace_id=trace_id):
                chosen_agent = BaseAgent(
                    name="Chatbot Agent",
                    deployment=model_options[st.session_state.model],
                )
                result = chosen_agent.execute_streamed(st.session_state.messages)
                answer = await stream_chat_message(result)
                st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    asyncio.run(app())
