import os
from config import CHARACTER_LIMIT


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Given a file path, provides the contents of that file, as long as it is within the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "A path to the file the contents of which will be read, relative to the working directory (default is the working directory itself)"
                }
            }
        }
    }
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        workdir_abs_path = os.path.abspath(working_directory)
        workdir_file_path = os.path.normpath(os.path.join(workdir_abs_path, file_path))

        if not (os.path.commonpath([workdir_abs_path, workdir_file_path]) == workdir_abs_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(workdir_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(workdir_file_path, "r") as f:
            file_content = f.read(CHARACTER_LIMIT)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'

            return file_content
    except Exception as e:
        return f"Something went wrong when reading the file, full error: {e}"
