import json
from os import environ
from typing import Union


def get_env(key) -> str:
    if key in environ:
        return environ[key]

    raise KeyError(f"Environment variable {key} is not set")


def read_json(filename: str, encoding: str = "utf-8"):
    with open(filename, encoding=encoding) as f:
        return json.load(f)
