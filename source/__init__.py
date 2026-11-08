from flask import Flask


def create_app(config) -> Flask:
    # app set up and configuration
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    from source.api import api_bp

    app.register_blueprint(api_bp)

    return app
