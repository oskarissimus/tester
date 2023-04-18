from os import environ, getenv

from tester.bash_process import BashProcess

bash = BashProcess(return_err_output=True)


def get_poetry_venv_from_project_path(
    bash: BashProcess, poetry_project_root: str
) -> str:
    venv_path = bash.run_sync(
        "poetry env info --path", cwd=poetry_project_root
    )
    venv_path_stripped = venv_path.strip()
    return venv_path_stripped


def get_poetry_venv_bin_path_from_project_path(
    bash: BashProcess, poetry_project_root: str
) -> str:
    venv_path = get_poetry_venv_from_project_path(bash, poetry_project_root)
    venv_bin_path = f"{venv_path}/bin"
    return venv_bin_path


def prepare_env_for_poetry_project(
    bash: BashProcess, poetry_project_root: str, current_env: dict
) -> dict:
    venv_bin_path = get_poetry_venv_bin_path_from_project_path(
        bash, poetry_project_root
    )
    new_path = f"{venv_bin_path}:{getenv('PATH')}"
    new_env = current_env.copy()
    new_env["PATH"] = new_path
    return new_env
