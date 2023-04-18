"""Wrapper around subprocess to run commands."""
import asyncio
import os
import subprocess
from typing import List, Union


class BashProcess:
    """Executes bash commands and returns the output."""

    def __init__(
        self, strip_newlines: bool = False, return_err_output: bool = False
    ):
        """Initialize with stripping newlines."""
        self.strip_newlines = strip_newlines
        self.return_err_output = return_err_output

    async def run(self, commands: Union[str, List[str]], cwd, env) -> str:
        """Run commands and return final output."""
        if isinstance(commands, str):
            commands = [commands]
        commands = ";".join(commands)
        try:
            proc = await asyncio.create_subprocess_shell(
                commands,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
                if self.return_err_output
                else asyncio.subprocess.STDOUT,
                cwd=cwd,
                executable="/bin/bash",
                env=env,
            )
            stdout, stderr = await proc.communicate()

            output = stdout.decode()
            if self.return_err_output and stderr:
                output += "\n" + stderr.decode()

            if proc.returncode != 0:
                raise subprocess.CalledProcessError(
                    proc.returncode, commands, output
                )

        except subprocess.CalledProcessError as error:
            if self.return_err_output:
                return output  # Zmień tutaj error.stderr na output
            return str(error)

        if self.strip_newlines:
            output = output.strip()
        return output

    def run_sync(
        self, commands: Union[str, List[str]], cwd, env=os.environ
    ) -> str:
        """Run commands synchronously and return final output."""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run(commands, cwd, env))
