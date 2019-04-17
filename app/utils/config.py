import os
import importlib

from app.utils.exceptions import UnknownKeyword


def get_config(env: str):
    if env.lower() not in ['local', 'test', 'production']:
        raise UnknownKeyword(env)
    os.environ['ENV'] = env
    config = importlib.import_module(f"config.{env}")
    return config
