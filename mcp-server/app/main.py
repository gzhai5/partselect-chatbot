import time
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain_community.callbacks.manager import get_openai_callback
from langgraph.pregel.io import AddableValuesDict
from loguru import logger
from app.utils import extract_summary
from app.service import service


# Create the app
app = FastAPI(title="MCP Server")


# set the CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # allow the cookie
    allow_methods=["*"],  # allow all http methods
    allow_headers=["*"],  # all all headers
)


# Home route
@app.get("/")
async def home():
    return {"message": "This is the back-end for the MCP Server"}

class QueryRequest(BaseModel):
    message: str
    sessionId: str

@app.post("/query")
async def process_query(request: QueryRequest):
    start_time = time.perf_counter()
    with get_openai_callback() as cb:
        response: AddableValuesDict = await service.ai_query(request.sessionId, request.message)
        logger.info(f"[OpenAI Usage - Total] Tokens: {cb.total_tokens}, Cost: ${cb.total_cost:.6f}")
        return extract_summary(request.message, response, cb, start_time)
    
@app.get("/tools")
async def get_tools():
    response = await service.get_tools()
    return response


# Exception handler
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )