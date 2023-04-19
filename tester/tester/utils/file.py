import json
from pathlib import Path


def file_writer(input, project_root):
    try:
        filename, file_contents = input.split("\n")[0], "\n".join(
            input.split("\n")[1:]
        )
        Path(f"{project_root}/{filename}").write_text(file_contents)
        return f"successfully wrote to file {filename}"
    except Exception as e:
        return f"failed to write to file {filename} with error {e}"


def file_reader(filename, project_root):
    try:
        file_contents = Path(f"{project_root}/{filename}").read_text()
        return f"file contents: {file_contents}"
    except Exception as e:
        return f"failed to read file {filename} with error {e}"
