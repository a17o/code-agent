import os


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        target_dir_path = os.path.normpath(os.path.join(working_dir_abs_path, directory))
        valid_target_dir_path = os.path.commonpath([target_dir_path, working_dir_abs_path]) == working_dir_abs_path

        if valid_target_dir_path is False:
            return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir_path):
            return f'\tError: "{directory}" is not a directory'

        lines = []
        for entry in sorted(os.scandir(target_dir_path), key=lambda e: e.name):
            lines.append(f"\t- {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}")

    except Exception as e:
        return f'\tError: something went wrong when getting the file info: {e}'

    return "\n".join(lines)
