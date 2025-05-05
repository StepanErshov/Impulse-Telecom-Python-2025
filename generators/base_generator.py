from abc import ABC, abstractmethod
import os
from datetime import datetime

class BaseGenerator(ABC):
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    @abstractmethod
    def generate(self, data: dict, output_dir: str) -> str:
        pass

    def _save_to_file(self, content: str, filename: str, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath