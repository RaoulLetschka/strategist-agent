# base.py
from agents import Agent, OpenAIChatCompletionsModel
from src.models.azure_openai_client import AzureOpenAIClient

class BaseAgent:
    def __init__(self, name: str, instructions: str, deployment: str, output_type=None):
        """
        Initialize the BaseAgent with the given parameters.
        :param name: The name of the agent.
        :param instructions: Instructions for the agent.
        :param deployment: The deployment name for the Azure OpenAI model.
        :param output_type: The type of output expected from the agent.
        """
        self.name = name
        self.agent = Agent(
            name=name,
            instructions=instructions,
            model=OpenAIChatCompletionsModel(
                model=deployment,
                openai_client=AzureOpenAIClient.create_client(),
            ),
            output_type=output_type,
        )

    async def execute(self, prompt: str):
        from src.core.runner import Runner
        result = await Runner.run(self.agent, prompt)
        return result.final_output