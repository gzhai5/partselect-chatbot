from pydantic import BaseModel, Field


class VerifyUserQueryRequest(BaseModel):
    query: str

class VerifyAIResponseRequest(BaseModel):
    query: str
    response: str

class VerifyUserQueryResponse(BaseModel):
    """Verifying if a user query is within the supported scope."""
    is_in_scope: bool = Field(description="Indicates if the query is within the supported scope: related to some general chatting or questions about the dishwasher or refrigerator from PartSelect. If asking other parts or appliances, it is also considered out of scope.")
    reason: str = Field(description="Explanation for why the query is or isn't within scope.")

class VerifyAIResponseResponse(BaseModel):
    """Verifying if an AI response is appropriate for a given user query."""
    is_appropriate: bool = Field(description="Indicates if the AI response is appropriate for the user query.")
    is_in_scope: bool = Field(description="Indicates if the user_query and AI response are within the supported scope: related to some general chatting or questions about the dishwasher or refrigerator from PartSelect. If asking other parts or appliances, it is also considered out of scope.")
    hallucination: bool = Field(description="Indicates if the AI response contains hallucinated information not supported by the provided context.")
    reason: str = Field(description="Explanation for why the AI response is or isn't appropriate for the user query.")