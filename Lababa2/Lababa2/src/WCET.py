#Вариант задания - Обработчик прерывания датчика: чтение, фильтрация, запись результата.
import json
import sys
from dataclasses import dataclass

#Название, тип, число обращений к памяти и ветвлений
@dataclass
class Operation:
    name: str
    type: str
    mem_accesses: int
    branches: int

#Базовая стоимость операции, штраф промаха кэша и штраф ошибки предсказания перехода (в тактах)
@dataclass
class Model:
    base_cost: int
    cache_miss_penalty: int
    branch_mispredict_penalty: int

#Лучшее время одной операции
def best_case(op: Operation, model: Model) -> int:
    return model.base_cost

#Худшее время одной операции
def worst_case(op: Operation, model: Model) -> int:
    return (model.base_cost
            + op.mem_accesses * model.cache_miss_penalty
            + op.branches * model.branch_mispredict_penalty)

#Сумма - лучшее время всех операций фрагмента (BCET)
def bcet(fragment: list[Operation], model: Model) -> int:
    return sum(best_case(op, model) for op in fragment)

#Сумма - худшее время всех операций фрагмента (WCET)
def wcet(fragment: list[Operation], model: Model) -> int:
    return sum(worst_case(op, model) for op in fragment)

#Расчет коэффициента недетерминизма
def nondeterminism_ratio(fragment: list[Operation], model: Model) -> float:
    return wcet(fragment, model) / bcet(fragment, model)

#Память и ветвления
def source_breakdown(fragment: list[Operation], model: Model) -> dict:
    memory = sum(op.mem_accesses for op in fragment) * model.cache_miss_penalty
    branches = sum(op.branches for op in fragment) * model.branch_mispredict_penalty
    return {"memory": memory, "branches": branches}

#Ввод
def load_file(path: str):
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    model = Model(**data["model"])
    fragment = [Operation(**o) for o in data["operations"]]
    return fragment, model, data["deadline"]

#Вывод
def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/variant.json"
    fragment, model, deadline = load_file(path)

    print(f"{'Операция':<40} | {'Тип':<7} | {'Лучшее':>6} | {'Худшее':>6}")
    print("-" * 68)
    for op in fragment:
        print(f"{op.name:<40} | {op.type:<7} | "
              f"{best_case(op, model):>6} | {worst_case(op, model):>6}")
    print("-" * 68)

    b, w = bcet(fragment, model), wcet(fragment, model)
    br = source_breakdown(fragment, model)
    print(f"BCET = {b} тактов")
    print(f"WCET = {w} тактов")
    print(f"Коэффициент недетерминизма = {nondeterminism_ratio(fragment, model):.2f}")
    print(f"Вклад памяти в наихудшее время: {br['memory']} тактов")
    print(f"Вклад ветвлений в наихудшее время: {br['branches']} тактов")
    print(f"Дедлайн = {deadline} тактов")
    if w <= deadline:
        print(f"Вывод: фрагмент УКЛАДЫВАЕТСЯ в дедлайн в худшем случае (запас {deadline - w}).")
    else:
        print(f"Вывод: фрагмент НЕ УКЛАДЫВАЕТСЯ в дедлайн в худшем случае (превышение {w - deadline}).")


if __name__ == "__main__":
    main()

