import json


def is_jsonable(value):
    try:
        json.dumps(value)
        return True
    except TypeError:
        return False


def jasonable_dict(arg_dict: dict) -> dict:
    jsonable = dict()
    for key, value in arg_dict.items():
        if is_jsonable(value):
            jsonable[key] = value
    return jsonable
