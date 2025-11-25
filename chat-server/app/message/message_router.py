from fastapi import APIRouter, HTTPException
from loguru import logger
from app.message.message_service import message_service
from app.message.interfaces import MessageStoreRequest


# define the router
router = APIRouter(prefix="/message", tags=["Message"])


@router.post("/send", response_description="Send a message, either from bot or user", status_code=201)
async def send_message(body: MessageStoreRequest):
    try:
        logger.debug(f"DEBUG: Received message request with body: {body.model_dump()}")
        response = message_service.send_message(
            id=body.id,
            sessionId=body.sessionId,
            sender=body.sender,
            content=body.content,
            action=body.action,
            timestamp=body.timestamp,
        )
        logger.info(f"INFO: Message sent successfully with id: {response['id']}")
        return response
    except HTTPException as http_e:
        logger.error(f"ERROR: HTTPException occurred when sending message: {http_e.detail}")
        raise http_e
    except Exception as e:
        logger.error(f"ERROR: An unexpected error occurred when sending message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred when sending message: {str(e)}") from e