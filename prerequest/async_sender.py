import asyncio
from request_obj import RequestObject
from typing import List

async def safe_request(semaphore: asyncio.Semaphore, request: RequestObject):
    async with semaphore:
        return await request.async_send()

async def prepre_request(list_requests: List[RequestObject], semaphore_reqs: int):
    semaphore = asyncio.Semaphore()
    sent_requests = []
    
    for request in list_requests:
        sent_requests.append(safe_request(semaphore, request))

    asyncio.gather(*sent_requests)