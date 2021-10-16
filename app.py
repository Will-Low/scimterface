from flask import Flask
from system import System
from scim import NotImplemented

app = Flask(__name__)


@app.route("/")
def hello_world():
    try:
        x = System()
        x.get_me()
        return "hello"
    except NotImplemented as err:
        return repr(err)
