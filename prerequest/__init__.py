from . import request_obj
from typing import List

class PrepareRequest(object):
    """
    A module to prepare requests before send
    """
    name: str
    pre_request: any
    tests: list
    variables: object
    request_list: List[request_obj.RequestObject]

    def __init__(self, name: str):
        self.collection_name = name
        self.variables = object()
        self.request_list = []

    def __str__(self) -> str:
        return f"{self.name}: [{len(self.request_list)}]"

    def set_variables(self, variables: dict):
        for key in variables:
            self.__setattr__(key, variables[key])

    def send(self):
        ...
    
    def async_send(self):
        ...