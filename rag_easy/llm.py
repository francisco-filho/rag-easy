import os
import re
import ollama
from pydantic import BaseModel
from openai import OpenAI
from typing import Union

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")

class LLM(BaseModel):
    model: str | None = DEFAULT_MODEL
    system: str | None = None 

class LLMOpenAI(LLM):
    api: Union[object, None] = None
    base_url: str = ""
    api_key: str = ""

    def __init__(self, model, system=None, base_url='http://localhost:11434/v1', api_key='ollama'):
        super().__init__(model=model, system=system, base_url=base_url, api_key=api_key)
        self.api = OpenAI(base_url=base_url, api_key=api_key)

    def chat(self, message, history=[], stream=False):
        history.append(dict(role='user', content=message))

        response = self.api.chat.completions.create(
            model=self.model,
            messages=history,
        )
        return response.choices[0].message.content

    

class LLMWithHistory(BaseModel):
    model: str | None = DEFAULT_MODEL
    system: str | None = None 
    messages: list[dict] = []

    def __init__(self, model=DEFAULT_MODEL, system_prompt=None):
        super().__init__(model=model, system_prompt=system_prompt)
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        print("reuslt", result)
        return result


class LLMOllamaWithHistory(LLMWithHistory):
    def __init__(self, model=DEFAULT_MODEL, system_prompt=None):
        super().__init__(model=model, system_prompt=system_prompt)
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def execute(self):
        response = ollama.chat(model=self.model, messages=self.messages)
        completion = response['message']['content']
        return completion

if __name__ == "__main__":
    llm = LLMOllamaWithHistory(system_prompt="You are a Java programmer. You do not explain, just write code")
    msg = llm.chat("Write code that calculate the 10 first fibonnaci numbers")
    print(msg)
    