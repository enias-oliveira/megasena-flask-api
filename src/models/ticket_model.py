from . import db


class TicketModel(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.BigInteger, primary_key=True)
    numbers = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
