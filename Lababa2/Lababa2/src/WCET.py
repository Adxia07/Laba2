import json
import sys
from dataclasses import dataclass

@dataclass
class Operation:
    name: str
    type: str
    mem_accesses: int
    branches: int

@dataclass
class Model:
    base_cost: int
    cache_miss_penalty: int
    branch_mispredict_penalty: int
