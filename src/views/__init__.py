from flask import Flask


def init_app(app: Flask):

    from .users_view import users_bp

    app.register_blueprint(users_bp)
