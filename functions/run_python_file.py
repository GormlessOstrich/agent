import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []

    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_target.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_target):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_target.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run([sys.executable, abs_target] + args, capture_output=True, cwd=working_directory, timeout=30, text=True)
        output = ""
        
        if result.stdout:
            output += f"STDOUT: {result.stdout.strip()}"
        if result.stderr:
            if output:
                output += "\n"
            output += f"STDERR: {result.stderr.strip()}"
        if result.returncode != 0:
            if output:
                output += "\n"
            output += f"Process exited with code {result.returncode}"
        if not output:
            return "No output produced."
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"