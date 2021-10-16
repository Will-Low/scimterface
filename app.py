from flask import Flask
from system import System

app = Flask(__name__)


@app.route("/")
def hello_world():
    try:
        x = System()
        x.get_me()
        return "hello"
    except NotImplementedError as err:
        return repr(err)
