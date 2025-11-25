import json
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger
from datetime import datetime
from app.utils.database import test_mongodb_connection
from app.conversation.conversation_router import router as conversation_router
from app.conversation.conversation_service import conversation_service
from app.message.message_router import router as message_router
from app.ai.ai_router import router as ai_router


# Create the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    test_mongodb_connection()
    logger.info("INFO: App started successfully")

    yield

    # shutdown logic
    logger.info("INFO: App stopped successfully")
app = FastAPI(title="Milea Chat BackEnd", lifespan=lifespan)


# set the CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # allow the cookie
    allow_methods=["*"],  # allow all http methods
    allow_headers=["*"],  # all all headers
)


# include the routers
app.include_router(conversation_router)
app.include_router(message_router)
app.include_router(ai_router)


# Home route
@app.get("/")
async def home():
    return {"message": "This is the back-end for the Milea Chat Server"}


# Exception handler
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# WebSocket route to monitor conversation lifecycle
@app.websocket("/ws/conversation/{session_id}")
async def conversation_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()
    print(f"[WS] Start conversation at {datetime.utcnow().isoformat()}")
    print(f"[WS] Conversation Session started: {session_id}")

    try:
        while True:
            msg = await websocket.receive_text()
            try:
                data = json.loads(msg)
                if data.get("type") == "ping":
                    print(f"[WS] Ping from Conversation session {session_id}")
                elif data.get("type") == "end":
                    print(f"[WS] Explicit end from Conversation session {session_id}")
            except json.JSONDecodeError:
                print(f"[WS] Invalid message: {msg}")
    except WebSocketDisconnect:
        print(f"[WS] Connection closed. Session ended: {session_id}")
        conversation_service.end_conversation_from_ws(session_id)