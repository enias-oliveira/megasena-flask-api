import json
from random import randint


def ticket_numbers_creator(numbers: int) -> list[int]:
    return [randint(1, 60) for n in range(numbers)]


def ticket_numbers_list_to_string(ticket_numbers: list[int]) -> str:
    return json.dumps(ticket_numbers)


def ticket_numbers_string_to_list(ticket_numbers: str) -> list[int]:
    return json.loads(ticket_numbers)
