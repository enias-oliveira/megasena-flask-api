from src.models.ticket_model import TicketModel

import json


def TicketSerializer(ticket: TicketModel) -> dict:
    ticket_numbers = ticket.ticket_numbers
    serialized_ticket = json.loads(ticket_numbers)

    return {
        "megasena_ticket_id": ticket.id,
        "ticket_numbers": serialized_ticket,
    }


def TicketsSerializer(tickets: list[TicketModel]) -> list[dict]:
    user_id = tickets[0].user_id
    return {
        "user_id": user_id,
        "megasena_tickets": [TicketSerializer(ticket) for ticket in tickets],
    }
