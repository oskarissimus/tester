from pathlib import Path

from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.llms import OpenAI
from langchain.tools import BaseTool
from langchain.utilities import BashProcess

bash = BashProcess()

llm = OpenAI(temperature=0)


def file_writer(input):
    filename = input.split("`")[1]
    file_contents = input.split("```")[1]
    Path(filename).write_text(file_contents)


tools = [
    Tool(
        name="Write to file",
        func=file_writer,
        description="useful for when you need to write contents to a file. The input to this tool should be a filename enclosed in single backticks, and then file contents enclosed in triple backticks. For example, `hello_world.py` ```print('hello world')``` would be the input if you wanted write hello world script to a file called hello_world.py.",
    ),
    Tool(
        name="show project structure",
        func=lambda x: bash.run("tree -I '__pycache__'"),
        description="shows the project structure",
    ),
    Tool(
        name="show file contents",
        func=lambda x: bash.run(f"cat {x}"),
        description="shows the contents of a file",
    ),
]


agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run("create file with python implementation of a rot13 algorithm")
