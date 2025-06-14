import requests
import json
import os

API_KEY = os.environ["OPENAI_API_KEY"]
API_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_weather(location, unit="fahrenheit"):
    print("Get weather tool called with location: ", location, " and unit: ", unit)
    return f"The weather in {location} is 22 degrees {unit}."

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

user_input = input("Enter your message: ")

messages = [
    {
        "role": "user", "content": user_input
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
        print("Tool call: ", tool_call)
        function_name = tool_call["function"]["name"]
        function_args = json.loads(tool_call["function"]["arguments"])


        if function_name == "get_current_weather":
            location = function_args.get("location")
            unit = function_args.get("unit", "celsius")

            function_response = get_weather(location, unit)


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
    print("Final response: ", assistant_message["content"])
