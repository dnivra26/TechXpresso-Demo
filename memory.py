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

memory = []

memory_file = "memory.json"

def add_memory(memory_entry):
    print("Add memory called with: ", memory_entry)
    memory.append(memory_entry)
    with open(memory_file, 'w') as file:
        json.dump(memory, file)
    return "OK"

def get_memory():
    print("Get memory called")
    with open(memory_file, 'r') as file:
        memory = json.load(file)
    return "\n".join(memory)

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_memory",
            "description": "Add an entry to the memory",
            "parameters": {
                "type": "object",
                "properties": {
                    "memory_entry": {
                        "type": "string",
                        "description": "memory entry to add"
                    }
                },
                "required": ["memory_entry"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_memory",
            "description": "Retrieve the content of the memory"
        }
    }
]

messages = [
    {
        
        "role": "system", "content": "You are a helpful assistant. Always call get_memory on the first interaction. When add_memory save with full context and not just one word"
    },
    {

        "role": "user", "content": "What is my name?"
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


            if function_name == "add_memory":
                memory_entry = function_args.get("memory_entry")


                function_response = add_memory(memory_entry)


                messages.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })

            elif function_name == "get_memory":
                


                function_response = get_memory()


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
        final_message = final_response_data["choices"][0]["message"]["content"]
        print(final_message)
    else:
        
        print(assistant_message["content"])
        break

