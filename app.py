from flask import abort, Flask

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


def get_system_file(system_name: str) -> str:
    cwd = os.getcwd()
    system_dir = cwd + "/systems"
    system_file = f"{system_dir}/{system_name}.py"
    return system_file


def load_module(system_name: str) -> str:
    system_file = get_system_file(system_name)
    module_name = f"systems.{system_name}"
    spec = importlib.util.spec_from_file_location(module_name, system_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module_name


class SystemSubclassMissing(Exception):
    def __init__(self, module_name):
        self.message = f'Module "{module_name}" is missing a subclass of System'


def get_system_subclass(module_name: str):
    """Does the file contain a subclass of System?"""
    module = sys.modules[module_name]
    for _, obj in inspect.getmembers(module):
        if not inspect.isclass(obj):
            continue
        if issubclass(obj, SCIMSystem):
            return obj
        raise SystemSubclassMissing(module_name)


@app.route("/<string:system_name>/<string:endpoint>")
def scim_endpoint(system_name: str, endpoint: str):
    check_system_name_exists(system_name)
    module_name = load_module(system_name)
    target_subclass = get_system_subclass(module_name)
    inst = target_subclass()
    return inst.get_groups()


def check_system_name_exists(system_name: str):
    """Confirm a file for the system name exists"""
    system_files = get_system_files()
    file_name_stems = [Path(f).stem for f in system_files]
    if system_name not in file_name_stems:
        abort(404)


def get_system_files() -> list[str]:
    cwd = os.getcwd()
    system_dir = cwd + "/systems"
    system_files = [f for f in glob.glob(system_dir + "/*.py")]
    return system_files


if __name__ == "__main__":
    app.run()
