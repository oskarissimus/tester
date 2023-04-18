from os import environ
from pathlib import Path

from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI

from tester.bash_process import BashProcess
from tester.utils import prepare_env_for_poetry_project

bash = BashProcess(return_err_output=True)
llm = ChatOpenAI()

PROJECT_ROOT = "/home/oskar/git/stressable"


def file_writer(input):
    try:
        filename, file_contents = input[0], input[1]
        Path(f"{PROJECT_ROOT}/{filename}").write_text(file_contents)
        return f"successfully wrote to file {filename}"
    except Exception as e:
        return f"failed to write to file {filename} with error {e}"


def file_reader(filename):
    try:
        file_contents = Path(f"{PROJECT_ROOT}/{filename}").read_text()
        return f"file contents: {file_contents}"
    except Exception as e:
        return f"failed to read file {filename} with error {e}"


def run_in_project_root(command):
    return bash.run_sync(
        command,
        cwd=PROJECT_ROOT,
    )


new_env = prepare_env_for_poetry_project(bash, PROJECT_ROOT, environ)


def run_in_project_root_with_env(command):
    return bash.run_sync(
        command,
        cwd=PROJECT_ROOT,
        env=new_env,
    )


tools = [
    Tool(
        name="write to file",
        func=file_writer,
        description="""useful for when you need to write contents to a file. The input to this tool should be a python list, for example: ["hello_world.py", "print('hello world')"]""",
    ),
    Tool(
        name="show project structure",
        func=lambda x: run_in_project_root("tree -I '__pycache__'"),
        description="shows the project structure",
    ),
    Tool(
        name="show file contents",
        func=file_reader,
        description="useful for when you need to see the contents of a file. The input to this tool should be a filename",
    ),
    Tool(
        name="run tests",
        func=lambda x: run_in_project_root_with_env("poetry run pytest"),
        description="useful for when you need to run tests",
    ),
]


agent = initialize_agent(
    tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)


agent.run(
    """
1. read file called `stressable/utils.py`")
2. show project structure
3. use pytest, write to file called `tests/test_utils.py` with unit tests for `stressable/utils.py`
4. run tests
"""
)
