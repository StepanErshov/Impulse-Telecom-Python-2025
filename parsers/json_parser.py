import json
from models.config_model import ConfigParameter

class JSONParser:
    @staticmethod
    def parse(json_content: str) -> list:
        data = json.loads(json_content)
        return [
            ConfigParameter(name=key, value=value)
            for key, value in data.items()
        ]