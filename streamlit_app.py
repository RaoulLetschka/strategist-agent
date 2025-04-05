import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from agents import Runner, set_default_openai_key, ItemHelpers, Agent
from openai.types.responses import ResponseTextDeltaEvent
from custom_agents.competitors_agent import competitors_agent
from manager import SWOTAnalysisManager

env_loaded = load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))

def initiate_default_session_state():
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = original_system_prompt

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if 'selected_agent' not in st.session_state:
        st.session_state.selected_agent = 0

agent_selectbox_options = [
    "Chatbot Agent",
    "Competitors Agent",
    "SWOT Agent",
    # "Financial Research Agent",
]

model_selectbox_options = [
    "gpt-4o-mini",
    "gpt-4o",
    "o3-mini",
]

def main_app_sidebar():
    st.sidebar.title("Choose Agent")
    st.session_state.selected_agent = st.sidebar.selectbox(
        "Select an agent",
        options=agent_selectbox_options,
        index=agent_selectbox_options.index("Chatbot Agent"),
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
        st.session_state.model = st.sidebar.selectbox(
            "Select a model",
            options=model_selectbox_options,
            index=model_selectbox_options.index("gpt-4o-mini"),
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
    print(st.session_state.messages)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Ask a question"):
        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        chosen_agent: Agent = Agent(
            name="Chatbot Agent",
            model=st.session_state.model,
        )
        if st.session_state.selected_agent == "Competitors Agent":
            chosen_agent = competitors_agent
        elif st.session_state.selected_agent == "SWOT Agent":
            chosen_agent = SWOTAnalysisManager()
        
            
        result = Runner.run_streamed(chosen_agent, st.session_state.messages)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("...")

            answer = ""
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    answer += event.data.delta
                    message_placeholder.markdown(answer, unsafe_allow_html=True)
                # elif event.type == "run_item_stream_event":
                #     if event.item.type == "tool_call_output_item":
                #         print(f"-- Tool output: {event.item.output}")
                #         message_placeholder.markdown(str(event.item.output), unsafe_allow_html=True)
                #         st.session_state.messages.append({"role": "assistant", "content": str(event.item.output)})

        st.session_state.messages.append({"role": "assistant", "content": answer})
        print(st.session_state.messages)
if __name__ == "__main__":
    asyncio.run(app())
