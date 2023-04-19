from langchain.agents import Tool

from tester.bash_process import BashProcess
from tester.utils.file import file_reader, file_writer

PROJECT_ROOT = "/home/oskar/git/stressable"
bash = BashProcess(return_err_output=True, cwd=PROJECT_ROOT)


tools = [
    Tool(
        name="write_file",
        func=lambda x: file_writer(x, PROJECT_ROOT),
        description="""useful for when you need to write contents to a file. The input to this tool should be filename\ncontents for example: hello_world.py\nprint('hello world')""",
    ),
    Tool(
        name="show_project_structure",
        func=lambda x: bash.run_sync("tree -I '__pycache__'"),
        description="shows the project structure",
    ),
    Tool(
        name="read_file",
        func=lambda x: file_reader(x, PROJECT_ROOT),
        description="useful for when you need to see the contents of a file. The input to this tool should be a filename",
    ),
    Tool(
        name="run_tests",
        func=lambda x: bash.run_sync("poetry run pytest"),
        description="useful for when you need to run tests",
    ),
    Tool(
        name="commit",
        func=lambda x: bash.run_sync(f"git commit -a -m '{x}'"),
        description="useful for when you need to commit changes input to this tool should be a commit message",
    ),
    Tool(
        name="add",
        func=lambda x: bash.run_sync(f"git add '{x}'"),
        description="useful for when you need to add files to the staging area. The input to this tool should be a filename",
    ),
    Tool(
        name="push",
        func=lambda x: bash.run_sync(f"git push --set-upstream origin '{x}'"),
        description="useful for when you need to push changes. The input to this tool should be a branch name",
    ),
    Tool(
        name="branch",
        func=lambda x: bash.run_sync(f"git checkout -b '{x}'"),
        description="useful for when you need to create a new branch. The input to this tool should be a branch name",
    ),
    Tool(
        name="pull_request",
        func=lambda x: bash.run_sync(f"gh pr create --fill --title '{x}'"),
        description="useful for when you need to create a pull request. The input to this tool should be a pull request title",
    ),
]
