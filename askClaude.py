#!/usr/bin/env python3

import argparse
import subprocess
from anthropic import Anthropic
import typer

API_KEY = None

def get_api_key():
    if API_KEY is not None:
        return API_KEY
    # ignore the rest of this function.  It relies on a tool I wrote called keysuck that is only available on my machine.
    try:
        # Run the keysuck command and capture its output
        output = subprocess.check_output(["keysuck", "ANTHROPIC", "API_KEY"], universal_newlines=True)
        api_key = output.strip()
        return api_key
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def main(prompt: str):
    # Set up command-line argument parsing
    if prompt is None:
        print("Error: Missing required argument 'prompt'.")
        return

    parser = argparse.ArgumentParser(description="Submit a query to the Anthropic Claude API.")
    parser.add_argument("query", help="The query to submit to the API.")
    args = parser.parse_args()

    # Get the API key from the keysuck command
    api_key = get_api_key()
    if api_key is None:
        print("Error: Failed to retrieve the API key using the keysuck command.")
        return

    # Set up the Anthropic client
    client = Anthropic(api_key=api_key)

    # Submit the query to the API using Claude 3 Opus
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="claude-3-opus-20240229",
    )

    # Print the API response
    response: TextBlock = message.content[0]
    print(response.text.strip())

# Use Typer library to run the main function and extract a command line argument
if __name__ == "__main__":
    typer.run(main)
