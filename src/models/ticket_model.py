from . import db


class TicketModel(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.BigInteger, primary_key=True)
    numbers = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    @property
    def ticket_numbers(self):
        from src.services.ticket_numbers import ticket_numbers_string_to_list

        return ticket_numbers_string_to_list(self.numbers)

    @ticket_numbers.setter
    def ticket_numbers(self, ticket_numbers: list[int]) -> None:
        from src.services.ticket_numbers import ticket_numbers_list_to_string

        self.numbers = ticket_numbers_list_to_string(ticket_numbers)
