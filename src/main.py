# main.py
import asyncio
from custom_agents.assistant_agent import GPT4oAgent, GPT4oMiniAgent

async def main():
    agent_gpt4o = GPT4oAgent()
    agent_o3mini = GPT4oMiniAgent()

    response_gpt4o = await agent_gpt4o.execute("Explain quantum computing briefly.")
    response_o3mini = await agent_o3mini.execute("Summarize today's news headlines.")

    print("GPT-4o response:", response_gpt4o)
    print("O3-mini response:", response_o3mini)

if __name__ == "__main__":
    asyncio.run(main())