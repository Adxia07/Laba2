import json
import sys
from dataclasses import dataclass

@dataclass
class Operation:
    name: str
    type: str
    mem_accesses: int
    branches: int
