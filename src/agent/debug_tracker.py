"""
Global debug tracker for tool calls
"""

_tool_calls = []


def clear():
    global _tool_calls
    _tool_calls = []


def get_all():
    global _tool_calls
    return _tool_calls


def track(tool_name, args, duration, success=True):
    global _tool_calls
    _tool_calls.append({
        "tool": tool_name,
        "args": args,
        "duration_seconds": round(duration, 3),
        "success": success
    })
