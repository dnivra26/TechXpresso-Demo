import requests
import json
import os
import subprocess
import sys

API_KEY = os.environ["OPENAI_API_KEY"]
API_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def list_files(directory_path):
    directory_path = directory_path.strip()
    print("List files called with directory path: ", directory_path)
    output = subprocess.check_output(["ls", directory_path]).decode(sys.stdout.encoding).strip()
    return output


def read_file(file_name):
    print("Read file called with file path: ", file_name)
    with open(file_name, 'r') as file:
        return file.read()

def edit_file(file_name, new_content):
    print("Edit file called with file path: ", file_name)
    new_content = new_content.strip()

    with open(file_name, 'w') as file:
        file.write(new_content)
    return "OK"

def create_file(file_name, content):
    print("Create file called with file path: ", file_name)
    content = content.strip()
    with open(file_name, 'w') as file:
        file.write(content)
    return "OK"


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
                "required": ["directory_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the content of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "name of the file to read"
                    }
                },
                "required": ["file_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Edit the content of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "name of the file to edit"
                    },
                    "new_content": {
                        "type": "string",
                        "description": "new content to write to the file"
                    }
                },
                "required": ["file_name", "new_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Create a new file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "name of the file to create"
                    },
                    "new_content": {
                        "type": "string",
                        "description": "content to write to the file"
                    }
                },
                "required": ["file_name", "new_content"]
            }
        }
    },
    
]

messages = [
    {
        "role": "user", "content": "create a fizz_buzz.py with a fizz_buzz function. Do not add any comment"
    }
]

payload = {
    "model": "gpt-4",
    "messages": messages,
    "tools": tools,
    "tool_choice": "auto"
}

while True:

    response = requests.post(API_URL, headers=headers, json=payload)
    response_data = response.json()


    assistant_message = response_data["choices"][0]["message"]
    messages.append(assistant_message)


    if "tool_calls" in assistant_message:
        for tool_call in assistant_message["tool_calls"]:
            print("Tool call: ", tool_call)
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

            elif function_name == "read_file":
                file_name = function_args.get("file_name")


                function_response = read_file(file_name)


                messages.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })

            elif function_name == "edit_file":
                file_name = function_args.get("file_name")
                content = function_args.get("new_content")



                function_response = edit_file(file_name, content)


                messages.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })

            elif function_name == "create_file":
                file_name = function_args.get("file_name")
                content = function_args.get("new_content")



                function_response = create_file(file_name, content)


                messages.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })


        payload = {
            "model": "gpt-4",
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto"
        }

        final_response = requests.post(API_URL, headers=headers, json=payload)
        final_response_data = final_response.json()
        print(final_response_data)
        final_message = final_response_data["choices"][0]["message"]["content"]
        print(final_message)
    else:
        
        print(assistant_message["content"])
        break

