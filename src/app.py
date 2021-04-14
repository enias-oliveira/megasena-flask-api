from flask import Flask


def create_app():
    app = Flask(__name__)

    from src.configurations import database, migration, serializers, authentication
    from src import configurations, views

    authentication.init_app(app)
    configurations.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    views.init_app(app)
    serializers.init_app(app)

    return app
