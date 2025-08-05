import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("--verbose", action="store_true")
    # user_arguments = sys.argv[1]
    
    args = parser.parse_args()  # Namespace with prompt and verbose attributes

    # if len(sys.argv) < 2:
        # print("You must provide a prompt!")
        # print("\nUsage: python main.py 'your prompt here'")
        # sys.exit(1)

    if args.verbose:
        print(f"User prompt: {args.prompt}")

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    # user_prompt = " ".join(user_prompt)
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)]),]
    
    i = 0
    while i < 20:
        try:
            response = generate_content(client, messages, args.verbose)
            
            has_function_calls = any(part.function_call for part in response.candidates[0].content.parts) # Check if the response has function calls.

            if not has_function_calls and response.text:
                print(f"Final response:")
                print(response.text)
                break # If there were function calls the loop continues.

        except Exception as e:
            print(f"Error: {e}")
            break
        
        i += 1
    
    # print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    # print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def generate_content(client, messages, verbose=False):
    # system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
    system_prompt = "You are a helpful AI coding agent. When a user asks a question or makes a request, make a function call plan. You can perform the following operations: - List files and directories, - Read file contents, - Execute Python files with optional arguments, - Write or overwrite files. All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. Assume relevant code is typically found in the 'calculator' directory."
    available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file])
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)
    messages.append(response.candidates[0].content)
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    for part in response.candidates[0].content.parts:
        if part.function_call:
            result = call_function(part.function_call, verbose)
            messages.append(result)
            if result.parts[0].function_response.response:
                if verbose:
                    print(f"-> {result.parts[0].function_response.response}")
            else:
                raise Exception("Expected function response not found")
    
    return response

def call_function(function_call_part, verbose=False):
    function_map = {"get_files_info": get_files_info, "get_file_content": get_file_content, "write_file": write_file, "run_python_file": run_python_file}

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    if function_call_part.name in function_map:
        function_to_call = function_map[function_call_part.name]
        function_call_part.args["working_directory"] = "./calculator"
        function_result = function_to_call(**function_call_part.args)
        
        return types.Content(role="tool", parts=[types.Part.from_function_response(name=function_call_part.name, response={"result": function_result},)],)
    else:
        return types.Content(role="tool", parts=[types.Part.from_function_response(name=function_call_part.name, response={"error": f"Unknown function: {function_call_part.name}"},)],)

if __name__ == "__main__":
    main()