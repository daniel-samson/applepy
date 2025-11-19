from flask import Flask

app = Flask("applepy")


@app.route("/", methods=["GET"])
def hello_world() -> dict[str, str]:
    return {"message": "Hello, World!"}

    return app
