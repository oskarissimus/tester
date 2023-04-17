from pathlib import Path

from langchain.agents import AgentType, Tool, initialize_agent
from langchain.llms import OpenAI
from langchain.utilities import BashProcess

bash = BashProcess(return_err_output=True)
llm = OpenAI(temperature=0)

PROJECT_ROOT = "/home/oskar/git/stressable"


def file_writer(input):
    filename = input.split("`")[1]
    file_contents = input.split("```")[1]
    try:
        Path(f"{PROJECT_ROOT}/{filename}").write_text(file_contents)
        return f"created file {filename}"
    except Exception as e:
        return f"failed to create file {filename} with error {e}"


def run_in_project_root(command):
    return bash.run(f"cd {PROJECT_ROOT} && {command}")


tools = [
    Tool(
        name="Write to file",
        func=file_writer,
        description="useful for when you need to write contents to a file. The input to this tool should be a filename enclosed in single backticks, and then file contents enclosed in triple backticks. For example, `hello_world.py` ```print('hello world')``` would be the input if you wanted write hello world script to a file called hello_world.py.",
    ),
    Tool(
        name="show project structure",
        func=lambda x: run_in_project_root("tree -I '__pycache__'"),
        description="shows the project structure",
    ),
    Tool(
        name="show file contents",
        func=lambda x: run_in_project_root(f"cat {x}"),
        description="useful for when you need to see the contents of a file. The input to this tool should be a filename",
    ),
]


agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)


agent.run("read file called `stressable/utils.py`")
agent.run("show project structure")
agent.run("create file with pytest unit tests for the code")
