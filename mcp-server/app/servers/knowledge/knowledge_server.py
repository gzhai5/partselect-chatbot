import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/')))
import requests
import httpx
from typing import Dict, Any
from openai import OpenAI
from mcp.server.fastmcp import FastMCP
from loguru import logger
from app.config import settings
from app.servers.knowledge.product_db_service import product_db
from app.service import service


mcp = FastMCP(
    name = "Knowledge",
    instructions = "Knowledge server for querying knowledge about dishwasher and refrigerator products",
    )

@mcp.tool()
async def get_product_data(part_number: str) -> Dict[str, Any]:
    """
    Get the product data based on the part number that is inside the query.
    The data contains information including the product name, price, PartSelect number, 
    manufacturer number, brand, installation difficulty, installation time, installation video,
    prodduct img url, text description, availability, replacement parts.
    The product will either be part from dishwasher or refrigerator category.
    Args:
        part_number (str): The part number of the product.
    Returns: 
        dict: A dictionary containing the product data or a not found message.
    """
    logger.info(f"⛏ <Tool Level> Tool: get_product_data, Part Number: {part_number}")
    try:
        product_part = product_db.find_product_by_number(part_number)
        if not product_part:
            logger.info(f"Product with part number {part_number} not found.")
            return { "found": False }
        else:
            cleaned_product_part = {k: v for k, v in product_part.items() if k != '_id'}
            logger.info(f"Product with part number {part_number} found: {cleaned_product_part}")
            return {
                "found": True,
                "product_data": str(cleaned_product_part),
                "product_img_url": cleaned_product_part.get("image_url", ""),
                "installation_video": cleaned_product_part.get("instal_video_url", "")
            }
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve product data: {e}")
        return { "found": False }
    
@mcp.tool()
async def web_search_using_openai(query: str) -> Dict[str, Any]:
    """
    Perform a web search using OpenAI's web search tool.
    This function should only be used when the product database does not contain the necessary information.
    It will leverage OpenAI's LLM and web search capabilities to find relevant information
    inside the commerce websites related to the query.
    Args:
        query (str): The search query.
    Returns:
        dict: A dictionary containing the web search suggestions.
    """
    logger.info(f"⛏ <Tool Level> Tool: web_search_using_openai, Query: {query}")
    try:
        api_key = settings.openai_api_key
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-5-nano",
            tools=[{"type": "web_search"}],
            input=query
        )
        logger.info(f"Web search response: {response.output_text}")
        return {
            'openai_web_search_suggestions': response.output_text
        }
    except httpx.RequestError as e:
        logger.error(f"Failed to perform web search: {e}")
        return {
            'openai_web_search_suggestions': "Web search failed due to an error."
        }
    
@mcp.tool()
async def semantic_search_for_repair_solutions(issue: str) -> Dict[str, Any]:
    """
    Perform a semantic search to find relevant repair solutions based on the issue description.
    This tool will only be used if the user directly asks for repair solutions on parts.
    This function searches the repair solutions database to find the most relevant solutions.
    Args:
        issue (str): The description of the issue.
    Returns:
        dict: A dictionary containing the top k relevant repair solutions.
    """
    logger.info(f"⛏ <Tool Level> Tool: semantic_search_for_repair_solutions, Issue: {issue}")
    try:
        response = service.answer_with_rag(user_issue=issue)
        logger.info(f"For the issue '{issue}', found repair solution: {response}")
        return {
            "found_solutions": True,
            "repair_solutions": response
        }
    except Exception as e:
        logger.error(f"Failed to perform semantic search: {e}")
        return { "found_solutions": False }
    

if __name__ == "__main__":
    mcp.run(transport="stdio")