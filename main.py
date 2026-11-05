import argparse
from email import message
from call_function import available_functions, call_function
from collections.abc import Iterable
from dotenv import load_dotenv
import json
import os
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam
from prompts import system_prompt
from typing import List

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

if api_key is None:
    raise RuntimeError("The API key is missing.")

def generate_content(client: OpenAI, messages: List) -> ChatCompletion:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if response.usage is None:
        raise RuntimeError("The request has failed. Please try again later.")

    return response


def loop(args, messages):
    for _ in range(5):
        response: ChatCompletion = generate_content(client, messages)
        response_message = response.choices[0].message
        messages.append(response_message)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}" \
                f"\nResponse tokens: {response.usage.completion_tokens}")

        tool_messages = []
        for tool_call in response.choices[0].message.tool_calls or []:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
            tool_message = call_function(tool_call, args.verbose)
            tool_messages.append(tool_message)

            if not tool_message["content"]:
                raise ValueError(f"Error: The content for {tool_call.function.name} call was empty.")

            if args.verbose:
                print(f"-> {tool_message['content']}")

        messages.extend(tool_messages)

        if response_message.content:
            print(f"Response:\n{response_message.content}")

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: Iterable[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    loop(args, messages)



if __name__ == "__main__":
    main()
