from request_obj import RequestObject
from typing import List

def make_request(list_requests: List[RequestObject]):
    for response in list_requests:
        response.send()