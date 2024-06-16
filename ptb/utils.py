import dataclasses
import inspect
import logging
from typing import AbstractSet, Any


def set_logging_httpx():
    # Enable logging
    logging.basicConfig(
        format="[%(asctime)s %(levelname)s] %(name)s - %(message)s", level=logging.INFO
    )
    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)


def all_subclasses(cls: Any) -> list:
    return cls.__subclasses__() + [
        g for s in cls.__subclasses__() for g in all_subclasses(s)
    ]


def argument_of(func) -> AbstractSet[str]:
    return inspect.signature(func).parameters.keys()


def from_dict(data_class, data):
    try:
        fieldtypes = {f.name: f.type for f in dataclasses.fields(data_class)}
        return data_class(**{f: from_dict(fieldtypes[f], data[f]) for f in data})
    except:
        return data
