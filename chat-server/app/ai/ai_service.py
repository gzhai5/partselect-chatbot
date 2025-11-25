from openai import OpenAI
from loguru import logger
from app.config import settings
from app.ai.interfaces import VerifyUserQueryResponse, VerifyAIResponseResponse

class AiService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        
    def verify_user_query(self, query: str) -> VerifyUserQueryResponse:
        fallback_response = VerifyUserQueryResponse(is_in_scope=False, reason="Unable to verify the query at this time.")
        try:
            response = self.client.responses.parse(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that verifies if a user query is within the supported scope: related to some general chatting or questions about the dishwasher or refrigerator from PartSelect. If asking other parts or appliances, it is also considered out of scope.",
                    },
                    {"role": "user", "content": "Is the following user query within the supported scope? Query: " + query},
                ],
                text_format=VerifyUserQueryResponse
            )
            parsed = response.output_parsed
            if not parsed:
                logger.error("Failed to parse AI response for user query verification.")
                return fallback_response
            logger.info(f"AI verification result: is_in_scope={parsed.is_in_scope}, reason={parsed.reason}")
            return parsed
        except Exception as e:
            logger.error(f"Error during AI verification of user query: {str(e)}")
            return fallback_response
    
    def verify_ai_response(self, query: str, response: str) -> VerifyAIResponseResponse:
        fallback_response = VerifyAIResponseResponse(
            is_appropriate=False,
            is_in_scope=False,
            hallucination=True,
            reason="Unable to verify the AI response at this time."
        )
        try:
            ai_response = self.client.responses.parse(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that verifies if an AI response is appropriate for a given user query. Also check if both the user query and AI response are within the supported scope: related to some general chatting or questions about the dishwasher or refrigerator from PartSelect. If asking other parts or appliances, it is also considered out of scope. Additionally, determine if the AI response contains hallucinated information not supported by the provided context.",
                    },
                    {"role": "user", "content": f"User Query: {query}\nAI Response: {response}\nIs the AI response appropriate for the user query?"},
                ],
                text_format=VerifyAIResponseResponse
            )
            parsed = ai_response.output_parsed
            if not parsed:
                logger.error("Failed to parse AI response for AI response verification.")
                return fallback_response
            logger.info(f"AI response verification result: is_appropriate={parsed.is_appropriate}, is_in_scope={parsed.is_in_scope}, hallucination={parsed.hallucination}, reason={parsed.reason}")
            return parsed
        except Exception as e:
            logger.error(f"Error during AI verification of AI response: {str(e)}")
            return fallback_response
    
ai_service = AiService()