from fastapi import APIRouter, HTTPException
from loguru import logger
from app.conversation.conversation_service import conversation_service
from app.conversation.interfaces import ConversationRequest


# define the router
router = APIRouter(prefix="/conversation", tags=["Conversation"])


@router.post("/begin", response_description="Begin a new conversation", status_code=201)
def begin_conversation(body: ConversationRequest):
    try:
        response = conversation_service.start_conversation(body.startTime, body.userId)
        logger.info(f"INFO: Conversation started successfully with sessionId: {response['sessionId']}")
        return response
    except HTTPException as http_e:
        logger.error(f"ERROR: HTTPException occurred when starting conversation: {http_e.detail}")
        raise http_e
    except Exception as e:
        logger.error(f"ERROR: An unexpected error occurred when starting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred when starting conversation: {str(e)}") from e
    

@router.post("/end", response_description="End a conversation", status_code=200)
def end_conversation(sessionId: str):
    try:
        response = conversation_service.end_conversation_from_api(sessionId)
        logger.info(f"INFO: Conversation ended successfully with sessionId: {sessionId}")
        return response
    except HTTPException as http_e:
        logger.error(f"ERROR: HTTPException occurred when ending conversation: {http_e.detail}")
        raise http_e
    except Exception as e:
        logger.error(f"ERROR: An unexpected error occurred when ending conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred when ending conversation: {str(e)}") from e