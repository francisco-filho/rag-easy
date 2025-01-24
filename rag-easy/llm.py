import ollama
from pydantic import BaseModel

default_model = "deepseek-r1:8b"

class LLM(BaseModel):
    model: str | None = default_model
    system: str | None = None 
    messages: list[dict] = []

    def __init__(self, model=default_model, system_prompt=None):
        super().__init__(model=model, system_prompt=system_prompt)
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result


class LLMOllama(LLM):
    def __init__(self, model=default_model, system_prompt=None):
        super().__init__(model=model, system_prompt=system_prompt)
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def execute(self):
        response = ollama.chat(model=self.model, messages=self.messages)
        completion = response['message']['content']
        return completion

if __name__ == "__main__":
    llm = LLMOllama(system_prompt="You are a Java programmer. You do not explain, just write code")
    msg = llm.chat("Write code that calculate the 10 first fibonnaci numbers")
    print(msg)
    