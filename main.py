import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    
    user_arguments = sys.argv[1]

    if len(sys.argv) < 2:
        print("You must provide a prompt!")
        print("\nUsage: python main.py 'your prompt here'")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(user_arguments)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    generate_content(client, messages)
    
    # print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    # print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def generate_content(client, messages):
    response = client.models.generate_content(model="gemini-2.0-flash-001",contents=messages,)

    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
