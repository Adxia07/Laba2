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

def best_case(op: Operation, model: Model) -> int:
    return model.base_cost

def worst_case(op: Operation, model: Model) -> int:
    return (model.base_cost
            + op.mem_accesses * model.cache_miss_penalty
            + op.branches * model.branch_mispredict_penalty)

def bcet(fragment: list[Operation], model: Model) -> int:
    return sum(best_case(op, model) for op in fragment)

def wcet(fragment: list[Operation], model: Model) -> int:
    return sum(worst_case(op, model) for op in fragment)

def nondeterminism_ratio(fragment: list[Operation], model: Model) -> float:
    return wcet(fragment, model) / bcet(fragment, model)

def source_breakdown(fragment: list[Operation], model: Model) -> dict:
    memory = sum(op.mem_accesses for op in fragment) * model.cache_miss_penalty
    branches = sum(op.branches for op in fragment) * model.branch_mispredict_penalty
    return {"memory": memory, "branches": branches}

