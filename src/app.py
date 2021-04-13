from flask import Flask


def create_app():
    app = Flask(__name__)

    from src import configurations, views

    configurations.init_app(app)
    views.init_app(app)

    @app.route("/")
    def hello_flask():
        return {"msg": "Hello Flask!"}

    return app
