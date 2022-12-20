from . import request_obj
from typing import List

class PrepareRequest(object):
    """
    A module to prepare requests before send
    """
    collection_name: str
    pre_request: any
    tests: list
    variables: object
    object_list: List[request_obj.ResponseObject]

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.variables = object()
        self.object_list = []

    def set_variables(self, variables: dict):
        for key in variables:
            self.__setattr__(key, variables[key])