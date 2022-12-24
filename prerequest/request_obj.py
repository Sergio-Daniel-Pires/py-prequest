from enum import Enum
import json
import requests

class EnumRequestType(Enum):
    MULTIPART = 'multipart/form-data'
    APPLICATION = 'application/json'

class EnumMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

class RequestObject(object):
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

    def __init__(self, name: str, url: str, method: EnumMethod, headers: dict, payload: dict = {}, files: dict = {}, **kwargs):
        self.name = name
        self.url = url
        self.method = method
        self.headers = headers
        self.payload = payload
        self.files = files
        self.request_type = EnumRequestType.MULTIPART

        self.session = kwargs.get('session', requests.Session)

        if kwargs.get("body_type") == EnumRequestType.APPLICATION or files == [] or files is None:
            self.request_type = EnumRequestType.APPLICATION
            self.payload.__setitem__('Content-Type', 'application/json')
            self.payload = json.dumps(self.payload)
            self.files = None

    def set_session(self, session: requests.Session):
        self.session = session

    def send(self, save_session: bool = False, **kwargs):
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
                file_path = kwargs.get('session_file', f'{self.name}-session.json')
                json.dump(current_session, open(file_path, 'w', encoding='utf8'))

        self.time_returned = datetime.now()

    async def async_send(self):
        from datetime import datetime
        self.time_sent = datetime.now()

        async with self.session() as current_session:
            async with current_session.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                data=self.payload,
                files=self.files
            ) as future_response:
                response = await future_response.json()
                self.time_returned = datetime.now()
                return response

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.name}"