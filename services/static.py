import os


def get_static_files():
    forbidden = []
    for path, _, files in os.walk("_public"):
        for name in files:
            forbidden.append(os.path.join(path, name))
    return forbidden
