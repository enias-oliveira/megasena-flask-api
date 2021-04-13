from flask import Flask


def create_app():
    app = Flask(__name__)

    from src.configurations import database, migration, serializers
    from src import configurations, views

    configurations.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    views.init_app(app)
    serializers.init_app(app)

    return app
