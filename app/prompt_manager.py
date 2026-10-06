import os
import yaml
from jinja2 import Template

class PromptManager:
    def __init__(self, prompts_dir="prompts"):
        self.prompts_dir = prompts_dir

    def load_prompt(self, name: str) -> dict:
        path = os.path.join(self.prompts_dir, f"{name}.yaml")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def render(self, name: str, **kwargs) -> list:
        """
        Render prompt with Jinja2 variables.
        Returns list of messages for LangChain/OpenAI.
        """
        prompt = self.load_prompt(name)
        messages = []
        for role, text in prompt.items():
            template = Template(text)
            rendered = template.render(**kwargs)
            messages.append({"role": role, "content": rendered})
        return messages

