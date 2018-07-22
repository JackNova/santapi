import os
import os.path
from functools import wraps
import json


def cached_in_db(func):
    """
    Decorator that caches the results of the function call.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = '-'.join(list(args) + list(kwargs.values()))
        path = f'db/{key}.json'
        if os.path.isfile(path):
            with open(path, 'r') as my_db:
                value_json = my_db.read()
                value = json.loads(value_json)
        else:
            value = func(*args, **kwargs)
            value_json = json.dumps(value, indent=4)
            with open(path, 'w') as my_db:
                my_db.write(value_json)

        return value

    return wrapper
