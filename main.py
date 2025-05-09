import requests
import os
import json

def convert_currency(source_currency: str, target_currency: str, amount: int):
    # actual implementation will go here
    return amount * 600

def tool_call_parser(output):
    for out in output:
        if out['type'] == 'function_call':
            args = json.loads(out['arguments'])
            function_output = convert_currency(args['source_currency'], args['target_currency'], args['amount'])
            print(function_output)

response = requests.post("https://api.openai.com/v1/responses",
                         headers={
                             "Authorization": f"Bearer {os.environ["OPENAI_API_KEY"]}",
                             "Content-Type": "application/json"
                         },
                         json={
                             "model": "gpt-4.1",
                             "input": "How much is 90 USD in INR",
                             "tools": [
                                 {
                                     "type": "function",
                                     "name": "convert_currency",
                                     "description": "Convert currency from one type to another.",
                                     "parameters": {
                                         "type": "object",
                                         "properties": {
                                             "source_currency": {
                                                 "type": "string",
                                                 "description": "The currency to convert from."
                                             },
                                             "target_currency": {
                                                 "type": "string",
                                                 "description": "The currency to convert to."
                                             },
                                             "amount": {
                                                 "type": "number",
                                                 "description": "The amount to convert."
                                             }
                                         },
                                         "required": [
                                             "source_currency",
                                             "target_currency",
                                             "amount"
                                         ],
                                         "additionalProperties": False
                                     }
                                 }
                             ]
                         })

print(response.json()['output'])
tool_call_parser(response.json()['output'])



