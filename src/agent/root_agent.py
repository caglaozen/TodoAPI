import os
import time

USE_STRANDS = os.getenv("USE_STRANDS", "false").lower() == "true"

import sys

if USE_STRANDS:
    from src.agent.todo_agent_strands import strands_todo_agent

    root_agent = strands_todo_agent
    print("🔵 Strands Agent active (for CLI/Web UI and MCP)", file=sys.stderr)
else:
    from src.agent.todo_agent import todo_agent

    root_agent = todo_agent
    print("🟢 Google ADK Agent active (for CLI/Web UI)", file=sys.stderr)

from . import debug_tracker


def clear_debug_info():
    debug_tracker.clear()


def get_debug_info():
    return debug_tracker.get_all()


def track_tool_call(tool_name, args, duration, success=True):
    debug_tracker.track(tool_name, args, duration, success)


def invoke_agent(message: str) -> str:
    """
    Programmatic agent invocation for MCP server.
    Works with both Strands and Google ADK agents.

    :param message: User message
    :return: Agent response as string
    """
    if USE_STRANDS:
        import asyncio
        import contextlib
        import io
        import litellm
        import warnings

        stdout_backup = sys.stdout
        stderr_backup = sys.stderr
        sys.stdout = io.StringIO()

        print(f"[STRANDS DEBUG] Starting agent with message: {message}", file=stderr_backup)

        try:
            result = root_agent(message)
            print(f"[STRANDS DEBUG] Agent completed, result type: {type(result)}", file=stderr_backup)

            if isinstance(result, dict) and "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    if isinstance(content[0], dict) and "text" in content[0]:
                        return content[0]["text"]
            return str(result)
        finally:
            sys.stdout = stdout_backup
            try:
                sys.stderr = io.StringIO()
                loop = asyncio.get_event_loop()
                if not loop.is_running():
                    loop.run_until_complete(litellm.close_litellm_async_clients())
                    loop.run_until_complete(asyncio.sleep(0.1))
            except Exception:
                pass
            finally:
                sys.stderr = stderr_backup
    else:
        import os
        from google.genai import Client
        from google.genai.types import FunctionResponse, Part

        client = Client(api_key=os.getenv("GOOGLE_API_KEY"))
        tools_config = [
            {
                "function_declarations": [
                    {
                        "name": func.__name__,
                        "description": func.__doc__ or func.__name__,
                        "parameters": {"type": "object"},
                    }
                    for func in root_agent.tools
                ]
            }
        ]

        chat = client.chats.create(model="gemini-2.0-flash", config={"tools": tools_config})
        response = chat.send_message(message)

        max_iterations = 10
        for iteration in range(max_iterations):
            if not response.candidates or not response.candidates[0].content.parts:
                break

            parts = response.candidates[0].content.parts
            function_calls = [p for p in parts if hasattr(p, "function_call") and p.function_call]

            if function_calls:
                function_responses = []
                for part in function_calls:
                    func_name = part.function_call.name
                    func_args = dict(part.function_call.args) if part.function_call.args else {}

                    tool_func = next((t for t in root_agent.tools if t.__name__ == func_name), None)
                    if tool_func:
                        result = tool_func(**func_args)
                        function_responses.append(
                            Part(function_response=FunctionResponse(name=func_name, response=result))
                        )

                if function_responses:
                    response = chat.send_message(function_responses)
                else:
                    break
            else:
                break

        return response.text if hasattr(response, "text") else str(response)
