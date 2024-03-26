import time
from typing import List

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from wiki2vid.config import Config


class AI:
    def __init__(self):
        self.chat = ChatOpenAI()

    def infer(self, messages: List[BaseMessage], filename: str = "progress.md") -> str:
        # Debug print
        if Config.verbosity >= 4:
            print(
                "-" * 50,
                "\n".join(str(message.content) for message in messages),
                "",
                sep="\n\n",
            )
        # Get the response and convert it to a string
        response = self.chat.invoke(messages)
        if isinstance(response.content, str):
            ret = response.content
        else:
            print("Got a list response from the model:")
            print(response.content)
            ret = str(response.content)
        # Debug print
        if Config.verbosity >= 4:
            print("-" * 50, ret, "-" * 50, sep="\n\n")
            time.sleep(Config.timeout_scalar)
        # Save the response to a file
        filepath = f"{Config.folder}/{filename}"
        if Config.save_intermediate or Config.interactive:
            with open(filepath, "w") as f:
                f.write(ret)
        # If we're not in interactive mode, just return the response
        if not Config.interactive:
            return ret
        # Otherwise, save the response to a file and prompt the user to edit it, then return the edited response
        print(f"Saved {filename}. Edit it as needed, then press Enter.")
        input()
        with open(filepath, "r") as f:
            return f.read()
