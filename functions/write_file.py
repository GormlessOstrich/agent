import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(name="write_file", description="Write or overwrite files.", parameters=types.Schema(type=types.Type.OBJECT, properties={"file_path": types.Schema(type=types.Type.STRING, description="The Python file's path, relative to the working directory.",), "content": types.Schema(type=types.Type.STRING, description="Text to be written to the file.",),},),)

def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_target.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    parent_dir = os.path.dirname(abs_target)
    
    try:
        os.makedirs(parent_dir, exist_ok=True)
        with open(abs_target, "w") as f:
            f.write(content)
    except Exception as e: 
        return f'Error: {str(e)}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'