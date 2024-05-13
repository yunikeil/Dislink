import os


def get_static_files():
    forbidden = []
    for path, _, files in os.walk("_public"):
        for name in files:
            forbidden.append(os.path.join(path, name))
    return forbidden


def is_static(name: str):
    """Check is name static file or other str"""
    static_path = os.path.normpath("_public/"+name)
    if static_path in get_static_files():
        return static_path
    return False