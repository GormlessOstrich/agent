import os

def get_files_info(working_directory, directory="."):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_target.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
    if not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'
    
    try:
        entries = []
        for name in os.listdir(abs_target):
            full_path = os.path.join(abs_target, name)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            entry_line = f"- {name}: file_size={file_size} bytes, is_dir={is_dir}"
            entries.append(entry_line)
        result = "\n".join(entries)   
        return result
    except Exception as e:
        return f"Error: {str(e)}"