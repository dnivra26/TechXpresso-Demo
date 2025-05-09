import requests
import json
import os
import subprocess

API_KEY = os.environ["OPENAI_API_KEY"]
API_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def list_files(directory_path):
    output = subprocess.check_output(["ls", directory_path])
    return output


def read_file():
    return ''

def write_file():
    return

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Get the list of files in a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "directory path from which to list the files"
                    }
                },
                "required": ["directory"]
            }
        }
    }
]

messages = [
    {
        "role": "user", "content": "What are the list of files in the directory /Users/arvindthangamani/projects/TechXpresso-Demo"
    }
]


payload = {
    "model": "gpt-4",
    "messages": messages,
    "tools": tools,
    "tool_choice": "auto"
}

response = requests.post(API_URL, headers=headers, json=payload)
response_data = response.json()


assistant_message = response_data["choices"][0]["message"]
messages.append(assistant_message)


if "tool_calls" in assistant_message:
    for tool_call in assistant_message["tool_calls"]:
        function_name = tool_call["function"]["name"]
        function_args = json.loads(tool_call["function"]["arguments"])


        if function_name == "list_files":
            directory = function_args.get("directory_path")


            function_response = list_files(directory)


            messages.append({
                "tool_call_id": tool_call["id"],
                "role": "tool",
                "name": function_name,
                "content": function_response
            })


    payload = {
        "model": "gpt-4",
        "messages": messages
    }

    final_response = requests.post(API_URL, headers=headers, json=payload)
    final_response_data = final_response.json()
    final_message = final_response_data["choices"][0]["message"]["content"]
    print(final_message)
else:
    # If no function call, print the assistant's message
    print(assistant_message["content"])
