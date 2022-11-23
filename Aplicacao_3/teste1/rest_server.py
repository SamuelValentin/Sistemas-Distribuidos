
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter, Request
from app.utils import status_event_generator

...

router = APIRouter()

@router.get('/status/stream')
async def runStatus(
        param1: str,
        request: Request
):
    event_generator = status_event_generator(request, param1)
    return EventSourceResponse(event_generator)