import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the specified python file within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the python file, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "optional list of strings",
                    "description": "Extra arguments needed to run the python program (if applicable)"
                }
            }
        }
    }
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        workdir_abs_path = os.path.abspath(working_directory)
        workdir_file_path = os.path.normpath(os.path.join(workdir_abs_path, file_path))

        if not os.path.commonpath([workdir_abs_path, workdir_file_path]) == workdir_abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not workdir_file_path.endswith(".py"):
                return f'Error: "{file_path}" is not a Python file'
        if not os.path.isfile(workdir_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'


        command = ["python", workdir_file_path]
        command.extend(args or [])

        completed_process = subprocess.run(command, text=True, timeout=30, capture_output=True)

        result = ""
        if completed_process.returncode != 0:
            result += f"Process exited with code {completed_process.returncode}\n"
        if len(completed_process.stderr) == 0 and len(completed_process.stdout) == 0:
            result += "No output produced\n"
        else:
            result += f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"

    return result
