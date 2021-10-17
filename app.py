from flask import Flask

import importlib.util
import inspect
import glob
import os
from pathlib import Path
import sys

from scim_system import SCIMSystem

app = Flask(__name__)


# For each system file, check to see if a class exists that is a subclass
# If so, make it available for call via the "scim_endpoint" function

def get_system_files() -> list[str]:
    cwd = os.getcwd()
    system_dir = cwd + "/systems"
    system_files = [f for f in glob.glob(system_dir + "/*.py")]
    return system_files


def import_systems(system_files: list[str]):
    for f in system_files:
        file_name_stem = Path(f).stem
        module_name = f"systems.{file_name_stem}"
        spec = importlib.util.spec_from_file_location(
            module_name,
            f
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        get_system_subclass(module_name)


class SystemSubclassMissing(Exception):
    def __init__(self, module_name):
        self.message = f"Module \"{module_name}\" is missing a subclass of System"


def get_system_subclass(module_name: str):
    """Does the file contain a subclass of System?"""
    module = sys.modules[module_name]
    for name, obj in inspect.getmembers(module):
        if not inspect.isclass(obj):
            continue
        if issubclass(obj, SCIMSystem):
            return obj
        raise SystemSubclassMissing(module_name)


@app.route("/")
def hello_world():
    try:
        x = System()
        x.get_me()
        return "hello"
    except NotImplemented as err:
        return repr(err)


@app.route("/<string:system_name>/<string:endpoint>")
def scim_endpoint(system_name: str, endpoint: str):
    systems = get_system_files()
    import_systems(systems)
    return f"{system_name}, {endpoint}"


if __name__ == "__main__":
    app.run()
