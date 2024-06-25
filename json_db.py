import contextlib
import json


@contextlib.contextmanager
def connect(path):
    d = {}

    with open(path, 'r') as f:
        d = json.loads(f.read())

    try:
        yield d
    finally:
        with open(path, 'w') as f:
            f.write(json.dumps(d, indent=2))
