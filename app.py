"""Contains the Flask app and module-loading logic"""

import importlib.util
import inspect
import glob
import os
from pathlib import Path
import sys
from typing import List

from flask import abort, Flask, request

from scim_system import SCIMSystem

app = Flask(__name__)


def get_system_file(system_name: str) -> str:
    """Gets the corresponding .py file, based on a system name"""
    cwd = os.getcwd()
    system_dir = cwd + "/systems"
    system_file = f"{system_dir}/{system_name}.py"
    return system_file


def load_module(system_name: str) -> str:
    """Loads the module designated by the system name"""
    system_file = get_system_file(system_name)
    module_name = f"systems.{system_name}"
    spec = importlib.util.spec_from_file_location(module_name, system_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module_name


class SystemSubclassMissing(Exception):
    """If an imported "systems" module doesn't have a subclass of SCIMSystem"""

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
    """Represents all SCIM endpoints, with a system-name prefix"""
    check_system_name_exists(system_name)
    module_name = load_module(system_name)
    target_subclass = get_system_subclass(module_name)
    inst = target_subclass()
    try:
        return call_method_and_endpoint_on_obj(request.method, endpoint, inst)
    except AttributeError:
        abort(404)


def check_system_name_exists(system_name: str):
    """Confirm a file for the system name exists"""
    system_files = get_system_files()
    file_name_stems = [Path(f).stem for f in system_files]
    if system_name not in file_name_stems:
        abort(404)


def get_system_files() -> List[str]:
    """Gets the list of all Python files in the "./systems/" directory"""
    cwd = os.getcwd()
    system_dir = cwd + "/systems"
    system_files = glob.glob(system_dir + "/*.py")
    return system_files


def call_method_and_endpoint_on_obj(
    method: str, endpoint: str, scim_system_obj: SCIMSystem
):
    """Given a method and a SCIM endpoint,
    calls the correspending method on the SCIMSystem object
    """
    method = get_lowercase_method(method)
    endpoint = get_endpoint(endpoint)
    function_method_to_call = getattr(scim_system_obj, f"{method}_{endpoint}")
    return function_method_to_call()


def get_lowercase_method(method: str) -> str:
    """Returns the lowercase name of the HTTP method"""
    return method.lower()


def get_endpoint(endpoint: str) -> str:
    """Returns the lowercase name of the SCIM endpoint"""
    return endpoint.strip("/").lower()


if __name__ == "__main__":
    app.run()
