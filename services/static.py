import os


def get_static_files():
    """
    {"name": "path"}
    """
    forbidden = {}
    for path, _, files in os.walk("_public"):
        for name in files:
            forbidden[name] = path
    return forbidden
