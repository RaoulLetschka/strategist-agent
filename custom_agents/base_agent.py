# base.py
from agents import Agent, OpenAIChatCompletionsModel, Runner
from .models.azure_openai_client import AzureOpenAIClient
from .config import settings

class BaseAgent:
    def __init__(
        self,
        name: str,
        deployment: str = settings.gpt4o_mini_deployment,
        instructions: str | None = None,
        output_type = None,
        model = None,
        **kwargs
    ):
        """
        Initialize the BaseAgent with the given parameters.
        :param name: The name of the agent.
        :param instructions: Instructions for the agent.
        :param deployment: The deployment name for the Azure OpenAI model.
        :param output_type: The type of output expected from the agent.
        """
        self.name = name
        self.model = model

        if model is None:
            self.agent = Agent(
                name=name,
                instructions=instructions,
                model=OpenAIChatCompletionsModel(
                    model=deployment,
                    openai_client=AzureOpenAIClient.create_async_client(),
                ),
                output_type=output_type,
                **kwargs
            )
        else:
            self.agent = Agent(
                name=name,
                instructions=instructions,
                model=model,
                output_type=output_type,
                **kwargs
            )

    async def execute(self, prompt: str):
        """
        Execute the agent with the given prompt.
        :param prompt: The prompt to execute.
        :return: The result of the agent execution.
        """
        # Ensure the agent is initialized
        if not self.agent:
            raise ValueError("Agent is not initialized.")
        # Ensure the prompt is provided
        if not prompt:
            raise ValueError("Prompt is required.")
        return await Runner.run(self.agent, prompt)
    
    def __str__(self):
        return f"Agent: {self.name}, Model: {self.model}, Instructions: {self.agent.instructions}"
    
    def __repr__(self):
        return f"BaseAgent(name={self.name}, model={self.model}, instructions={self.agent.instructions})"
    
    def __hash__(self):
        return hash((self.name, self.model, self.agent.instructions))
    
    def __eq__(self, other):
        if not isinstance(other, BaseAgent):
            return False
        return (
            self.name == other.name
            and self.model == other.model
            and self.agent.instructions == other.agent.instructions
        )
