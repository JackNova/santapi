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


def cache_in_calendar(func):
    
    def wrapper(*args, **kwargs):
        month = kwargs.get('month')
        day = kwargs.get('day')
        if not month or not day:
            raise Exception("missing month or day kwargs")
        key = "{:02d}/{:02d}".format(month, day)
        path = f'calendar/{key}.json'
        if os.path.isfile(path):
            with open(path, 'r') as my_db:
                value_json = my_db.read()
                value = json.loads(value_json)
        else:
            value = func(*args, **kwargs)
            value_json = json.dumps(value, indent=4)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as my_db:
                my_db.write(value_json)

        return value

    return wrapper
