from flask import Flask


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask("applepy")

    @app.route("/", methods=["GET"])
    def hello_world() -> dict[str, str]:
        return {"message": "Hello, World!"}

    return app


app = create_app()
