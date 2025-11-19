from flask import Flask

app = Flask("applepy")


@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"
