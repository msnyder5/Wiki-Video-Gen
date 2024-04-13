import os
import time
from typing import Callable, List, Optional

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from wiki2vid.config import Config

# Models:
# gpt-4-0125-preview
# gpt-3.5-turbo


class AI:
    chat = ChatOpenAI(model=Config.llm_model)

    @staticmethod
    def infer(
        messages: List[BaseMessage],
        filepath: Optional[str] = None,
        reuse=True,
        formatter: Callable[[str], str] = lambda x: x,
    ) -> str:
        # Check if the response is already saved
        if reuse and filepath and os.path.exists(filepath):
            with open(filepath, "r") as f:
                return f.read()

        # Get the response and convert it to a string
        response = AI.chat.invoke(messages)
        if isinstance(response.content, str):
            ret = response.content
        else:
            print("Got a list response from the model:")
            print(response.content)
            ret = str(response.content)

        ret = formatter(ret)

        # Return the response if no filepath is provided
        if not filepath:
            return ret

        # Save the response to a file if needed
        if Config.save_intermediate or Config.interactive:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w") as f:
                f.write(ret)

        # If we're not in interactive mode, just return the response
        if not Config.interactive:
            return ret

        # Otherwise, save the response to a file and prompt the user to edit it, then return the edited response
        print(f"Saved {filepath}. Edit it as needed, then press Enter.")
        input()
        with open(filepath, "r") as f:
            return f.read()
