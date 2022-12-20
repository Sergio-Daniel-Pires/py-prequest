from enum import Enum
import json
import requests

class EnumRequestType(Enum):
    MULTIPART = 'multipart/form-data'
    APPLICATION = 'application/json'

class EnumMethod(Enum):
    GET = "GET"
    POST = "POST"

class ResponseObject(object):
    name: str
    url: str
    auth: any
    headers: dict
    method: str
    payload: dict
    files: dict
    request_type: EnumRequestType
    session: requests.Session

    size: float
    time_sent: str
    time_returned: str
    response: dict

    def __init__(self, name: str, url: str, method: EnumMethod, headers: dict, payload: dict = {}, files: dict = {}):
        self.name = name
        self.url = url
        self.method = method
        self.headers = headers
        self.payload = payload
        self.files = files
        self.request_type = EnumRequestType.MULTIPART

        self.session = requests.Session

        if files == {}:
            self.request_type = EnumRequestType.APPLICATION
            self.payload.__setitem__('Content-Type', 'application/json')
            self.payload = json.dumps(self.payload)
            self.files = None


    def set_session(self, session: requests.Session):
        self.session = session

    def send(self, save_session: bool = False):
        from datetime import datetime
        self.time_sent = datetime.now()
        
        with self.session() as current_session:
            response = current_session.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                data=self.payload,
                files=self.files
            )
            self.response = response

            if save_session:
                json.dump(current_session, open(f'{self.name}-session.json', 'w', encoding='utf8'))

        self.time_returned = datetime.now()

    def __str__(self):
        return f"{self.name}: {self.url}"