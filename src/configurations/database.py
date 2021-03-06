from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from src.models.user_model import UserModel

    from src.models.ticket_model import TicketModel
