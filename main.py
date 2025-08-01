import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    generate_content(client, messages, args.verbose)
    
    # print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    # print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(model="gemini-2.0-flash-001",contents=messages,)
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
