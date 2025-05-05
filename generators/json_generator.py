import json
from .base_generator import BaseGenerator

class JSONGenerator(BaseGenerator):
    def generate(self, data: dict, output_dir: str) -> str:
        filename = f"config_{self.timestamp}.json"
        json_content = json.dumps(data, indent=4, ensure_ascii=False)
        return self._save_to_file(json_content, filename, output_dir)