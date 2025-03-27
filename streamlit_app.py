import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from agents import Runner, set_default_openai_key, ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent
from custom_agents.competitors_agent import competitors_agent

env_loaded = load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))

def initiate_default_session_state():
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = original_system_prompt

    if "messages" not in st.session_state:
        st.session_state.messages = []

def main_app_sidebar():
    st.sidebar.title("Options")

    st.sidebar.title("Change System Prompt")
    if st.sidebar.button("Reset System Prompt"):
        st.session_state.system_prompt = original_system_prompt
    st.session_state.user_prompt = st.sidebar.text_area(
        "System Prompt", 
        value=st.session_state.system_prompt, 
        height=200, 
        key="system_prompt"
    )

original_system_prompt = """You are an expert strategist for a company. 
You are tasked with determining the top competitors for the company based on its sector or industry.
The company has provided you with the the name of the company or the Yahoo Finance ticker symbol of the company. 
Your goal is to make a competitor analysis with the SWOT framework.
"""

async def app():
    initiate_default_session_state()

    main_app_sidebar()

    st.title("Strategist Agent")
    st.sidebar.button("Clear Chat", on_click=lambda: st.session_state.update(messages=[]))

    competitors_agent.instructions = st.session_state.system_prompt

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Ask a question"):
        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        result = Runner.run_streamed(competitors_agent, prompt)

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

if __name__ == "__main__":
    asyncio.run(app())
