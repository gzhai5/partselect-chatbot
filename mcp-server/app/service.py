from collections import defaultdict
from loguru import logger
from openai import OpenAI
from pymongo import MongoClient
from app.config import settings
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.graph import CompiledGraph
from pydantic import BaseModel
from app.prompt import build_agent_prompt
from app.mcpclient.config import mcpclient_config


class ProductData(BaseModel):
    name: str
    partselect_number: str
    manufacturer_number: str
    price: float
    installation_difficulty: str
    installation_time: str
    installation_video_url: str
    product_image_url: str
    brand: str
    replace_parts: list[str]
    availability: str
    symptoms: list[str]
    description: str

class AgentResponse(BaseModel):
    message: str
    product_data: ProductData | None = None

class Service:
    def __init__(self):
        self.session_agent_map = defaultdict(CompiledGraph) # session_id -> agent
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-4.1-mini"
        self.mongo = MongoClient(settings.mongo_uri)
        self.db = self.mongo["Product"]
        self.solutions_col = self.db["Repairs"]

    async def ai_query(self, session_id: str, query: str):
        if session_id in self.session_agent_map:
            agent = self.session_agent_map[session_id]
        else:
            agent = await self._setup_ai_agent()
        response = await agent.ainvoke({"messages": query}, config={"configurable": {"thread_id": session_id}})
        self.session_agent_map[session_id] = agent
        return response

    @staticmethod
    async def _setup_ai_agent(model_name: str = "deepseek-chat"):
        client = MultiServerMCPClient(mcpclient_config)
        tools = await client.get_tools()
        checkpointer = InMemorySaver()
        agent = create_react_agent(
            model=model_name, 
            tools=tools, 
            prompt=build_agent_prompt(),
            checkpointer=checkpointer,
            response_format=AgentResponse.model_json_schema()
        )
        return agent
    
    async def get_tools(self):
        client = MultiServerMCPClient(mcpclient_config)
        tools = await client.get_tools()
        return [
            {"name": tool.name, "description": tool.description.strip()}
            for tool in tools
        ]

    def embed_query(self, query: str):
        resp = self.client.embeddings.create(
            model=self.embedding_model,
            input=[query],
        )
        return resp.data[0].embedding

    def search_solutions(self, query: str, k: int = 5):
        q_vec = self.embed_query(query)

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "solutions_embedding_index",  # name from step 3
                    "path": "embedding",
                    "queryVector": q_vec,
                    "numCandidates": 100,
                    "limit": k
                }
            },
            {
                "$project": {
                    "appliance": 1,
                    "category": 1,
                    "part": 1,
                    "solution": 1,
                    "issue_description_url": 1,
                    "video_url": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        return list(self.solutions_col.aggregate(pipeline))

    def answer_with_rag(self, user_issue: str, k: int = 3) -> str:
        hits = self.search_solutions(user_issue, k=k)

        context_blocks = []
        for h in hits:
            context_blocks.append(
                f"[Part: {h.get('part')} | Category: {h.get('category')} "
                f"| Score: {h.get('score', 0):.3f}]\n"
                f"{h.get('solution','')}\n"
                f"Issue URL: {h.get('issue_description_url','')}\n"
                f"Video URL: {h.get('video_url','')}"
            )
        context_text = "\n\n-----\n\n".join(context_blocks)

        system_prompt = (
            "You are an appliance repair assistant. "
            "Use ONLY the provided context to answer. "
            "Explain steps clearly, referencing the part names."
            "Your response must be in Markdown format."
            "If you include any links, format them using Markdown syntax: [link text](URL)."
        )

        user_prompt = (
            f"User issue:\n{user_issue}\n\n"
            f"Relevant solutions from database:\n{context_text}\n\n"
            "What should the user check and how should they test or replace the parts?"
        )

        resp = self.client.responses.create(
            model=self.chat_model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return resp.output_text

service = Service()