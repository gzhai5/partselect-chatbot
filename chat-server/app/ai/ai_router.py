from fastapi import APIRouter, HTTPException
from loguru import logger
from app.ai.ai_service import ai_service
from app.ai.interfaces import VerifyUserQueryRequest, VerifyAIResponseRequest


# define the router
router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/verify-user-query", response_description="Verify user query", status_code=200)
def verify_user_query(body: VerifyUserQueryRequest):
    try:
        response = ai_service.verify_user_query(body.query)
        logger.info(f"INFO: User query verified successfully.")
        return response
    except HTTPException as http_e:
        logger.error(f"ERROR: HTTPException occurred when verifying user query: {http_e.detail}")
        raise http_e
    except Exception as e:
        logger.error(f"ERROR: An unexpected error occurred when verifying user query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred when verifying user query") from e
    
@router.post("/verify-ai-response", response_description="Verify AI response", status_code=200)
def verify_ai_response(body: VerifyAIResponseRequest):
    try:
        response = ai_service.verify_ai_response(body.query, body.response)
        logger.info(f"INFO: AI response verified successfully.")
        return response
    except HTTPException as http_e:
        logger.error(f"ERROR: HTTPException occurred when verifying AI response: {http_e.detail}")
        raise http_e
    except Exception as e:
        logger.error(f"ERROR: An unexpected error occurred when verifying AI response: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred when verifying AI response") from e
        