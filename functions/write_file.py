import os


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes the supplied text into a file within the working directory, overwriting the text in it. If the file does not exist, creates the file and subdirectories if necessary",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write to, relative to the working directory"
                },
                "content": {
                    "type": "string",
                    "description": "The text content that will be written to the file"
                }
            }
        }
    }
}

def write_file(working_directory: str, file_path: str, content: str):
    try:
        workdir_abs_path = os.path.abspath(working_directory)
        workdir_file_path = os.path.normpath(os.path.join(workdir_abs_path, file_path))

        if not (os.path.commonpath([workdir_abs_path, workdir_file_path]) == workdir_abs_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(workdir_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        if not os.path.isfile(workdir_file_path):
            os.makedirs(os.path.dirname(workdir_file_path), exist_ok=True)

        with open(workdir_file_path, "w") as f:
            f.write(content)

    except Exception as e:
        return f'Error: something went wrong, details: {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
