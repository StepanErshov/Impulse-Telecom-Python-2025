from dataclasses import dataclass
from typing import List, Dict

@dataclass
class UMLClass:
    name: str
    is_root: bool
    documentation: str
    attributes: List[Dict[str, str]]

@dataclass
class Aggregation:
    source: str
    target: str
    source_multiplicity: str
    target_multiplicity: str