from flask import Flask


def init_app(app: Flask):

    from .users_view import users_bp

    app.register_blueprint(users_bp)

    from .megasenas_view import megasenas_bp

    app.register_blueprint(megasenas_bp)
