import time
from langchain_community.callbacks.openai_info import OpenAICallbackHandler
from langgraph.pregel.io import AddableValuesDict


def extract_summary(query: str, response: AddableValuesDict, cb: OpenAICallbackHandler, start_time: float):
    messages = response.get("messages", [])
    
    # Get the final AI message with content
    final_ai = next((msg for msg in reversed(messages) if msg.type == "ai" and msg.content), None)

    # Get what tools were used
    tools = [msg.tool_calls if hasattr(msg, "tool_calls") else [] for msg in messages if msg.type == "ai"]
    tools = [tool for sublist in tools for tool in sublist]
    
    # Extract token usage
    token_usage = {
        "completion_tokens": cb.completion_tokens,
        "prompt_tokens": cb.prompt_tokens,
        "total_tokens": cb.total_tokens
    }

    return {
        "query": query,
        "answer": final_ai.content if final_ai else "",
        "token_usage": token_usage,
        "total_price": cb.total_cost,
        "response_time": str(round((time.perf_counter() - start_time) * 1000, 2)) + " ms",
        "tools_used": tools
    }