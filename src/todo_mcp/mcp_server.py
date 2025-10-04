import asyncio
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

asyncio_logger = logging.getLogger("asyncio")
asyncio_logger.setLevel(logging.CRITICAL)

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from src.config.mcp_config import MCP_SERVER_NAME, MCP_SERVER_VERSION, TOOL_DESCRIPTIONS
from src.todo_mcp.tools import todo_tools

server = Server(MCP_SERVER_NAME)

logger.info(f"🎯 MCP Server initialized: {MCP_SERVER_NAME}")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Handler for listing available tools.

    :return: List of available tools with their schemas
    """
    logger.info("📋 Listing available tools...")

    return [
        types.Tool(
            name="list_todos",
            description=TOOL_DESCRIPTIONS["list_todos"],
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="create_todo",
            description=TOOL_DESCRIPTIONS["create_todo"],
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title of the todo item (required)"},
                    "description": {
                        "type": "string",
                        "description": "Additional details about the todo (optional, default: empty)",
                    },
                    "due_date": {
                        "type": "string",
                        "description": "When the todo is due. Can be 'today', 'tomorrow', 'next week', or YYYY-MM-DD format (optional, default: next week)",
                    },
                },
                "required": ["title"],
            },
        ),
        types.Tool(
            name="get_todo_details",
            description=TOOL_DESCRIPTIONS["get_todo_details"],
            inputSchema={
                "type": "object",
                "properties": {"item_id": {"type": "string", "description": "The unique ID of the todo item"}},
                "required": ["item_id"],
            },
        ),
        types.Tool(
            name="update_todo",
            description=TOOL_DESCRIPTIONS["update_todo"],
            inputSchema={
                "type": "object",
                "properties": {
                    "item_id": {"type": "string", "description": "The unique ID of the todo to update"},
                    "title": {"type": "string", "description": "New title (optional)"},
                    "description": {"type": "string", "description": "New description (optional)"},
                    "due_date": {
                        "type": "string",
                        "description": "New due date - can be 'today', 'tomorrow', 'next week', or YYYY-MM-DD (optional)",
                    },
                },
                "required": ["item_id"],
            },
        ),
        types.Tool(
            name="mark_completed",
            description=TOOL_DESCRIPTIONS["mark_completed"],
            inputSchema={
                "type": "object",
                "properties": {
                    "item_id": {"type": "string", "description": "The unique ID of the todo to mark as completed"}
                },
                "required": ["item_id"],
            },
        ),
        types.Tool(
            name="delete_todo",
            description=TOOL_DESCRIPTIONS["delete_todo"],
            inputSchema={
                "type": "object",
                "properties": {"item_id": {"type": "string", "description": "The unique ID of the todo to delete"}},
                "required": ["item_id"],
            },
        ),
        types.Tool(
            name="search_todos",
            description=TOOL_DESCRIPTIONS["search_todos"],
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keyword or phrase to look for in todo titles and descriptions",
                    }
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="strands_assistant",
            description=TOOL_DESCRIPTIONS["strands_assistant"],
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Natural language request in English or Turkish. Examples: 'kitap okumayı 3 saat yap ve yemek yapmayı sil', 'create 3 todos and delete completed ones', 'find work todos and mark done'",
                    }
                },
                "required": ["message"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handler for tool execution requests.

    :param name: Tool name (e.g., "list_todos")
    :param arguments: Tool parameters (dict or None)
    :return: Tool execution result as TextContent
    """
    logger.info(f"🔧 Tool called: {name}")
    logger.info(f"   Arguments: {arguments}")

    if arguments is None:
        arguments = {}

    try:
        if name == "list_todos":
            result = todo_tools.list_all_todos()

        elif name == "create_todo":
            result = todo_tools.create_todo(
                title=arguments.get("title", ""),
                description=arguments.get("description", ""),
                due_date=arguments.get("due_date", ""),
            )

        elif name == "get_todo_details":
            result = todo_tools.get_todo_details(item_id=arguments.get("item_id", ""))

        elif name == "update_todo":
            result = todo_tools.update_todo(
                item_id=arguments.get("item_id", ""),
                title=arguments.get("title"),
                description=arguments.get("description"),
                due_date=arguments.get("due_date"),
            )

        elif name == "mark_completed":
            result = todo_tools.mark_completed(item_id=arguments.get("item_id", ""))

        elif name == "delete_todo":
            result = todo_tools.delete_todo(item_id=arguments.get("item_id", ""))

        elif name == "search_todos":
            result = todo_tools.search_todos(query=arguments.get("query", ""))

        elif name == "strands_assistant":
            from src.agent import invoke_agent

            user_message = arguments.get("message", "")
            logger.info(f"🤖 Strands assistant called with message: {user_message}")

            try:
                agent_response = invoke_agent(user_message)
                result = {
                    "status": "success",
                    "message": "Strands assistant completed",
                    "response": str(agent_response),
                }
                logger.info(f"✨ Strands response: {str(agent_response)[:200]}...")
            except Exception as e:
                result = {
                    "status": "error",
                    "message": f"Strands assistant error: {str(e)}",
                }
                logger.error(f"❌ Strands assistant error: {e}", exc_info=True)

        else:
            result = {"status": "error", "message": f"Unknown tool: {name}"}
            logger.error(f"❌ Unknown tool requested: {name}")

        result_json = json.dumps(result, ensure_ascii=False, indent=2)
        logger.info(f"✅ Tool result: {result_json[:100]}...")

        return [types.TextContent(type="text", text=result_json)]

    except Exception as e:
        error_msg = f"Error executing tool '{name}': {str(e)}"
        logger.error(f"❌ {error_msg}", exc_info=True)

        return [types.TextContent(type="text", text=json.dumps({"status": "error", "message": error_msg}))]


async def main():
    """
    Start the MCP server via stdio communication.

    :return: None
    """
    logger.info("=" * 60)
    logger.info("🚀 Starting MCP Server for Todo API")
    logger.info("=" * 60)
    logger.info("📝 Available tools (8 total):")
    logger.info("   1. list_todos - List all todo items")
    logger.info("   2. create_todo - Create a new todo")
    logger.info("   3. get_todo_details - Get details of a specific todo")
    logger.info("   4. update_todo - Update a todo")
    logger.info("   5. mark_completed - Mark a todo as completed")
    logger.info("   6. delete_todo - Delete a todo")
    logger.info("   7. search_todos - Search todos with Elasticsearch")
    logger.info("   8. strands_assistant ⭐ - AI-powered multi-step reasoning")
    logger.info("=" * 60)
    logger.info("🔗 Waiting for MCP client connections (stdin/stdout)...")
    logger.info("=" * 60)

    init_options = InitializationOptions(
        server_name=MCP_SERVER_NAME,
        server_version=MCP_SERVER_VERSION,
        capabilities=server.get_capabilities(notification_options=NotificationOptions(), experimental_capabilities={}),
    )

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("✅ stdio server started, running MCP protocol...")
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Server stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}", exc_info=True)
        sys.exit(1)
