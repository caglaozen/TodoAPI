import sys
import time
import os
from strands import tool

from . import todo_tools
from . import debug_tracker


@tool
def list_all_todos() -> dict:
    """
    Lists all todo items.

    :return: Todo list with status and count information
    """
    print("[TOOL CALL] list_all_todos", file=sys.stderr)
    start = time.time()
    try:
        result = todo_tools.list_all_todos()
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("list_all_todos", {}, time.time() - start, success=True)
        return result
    except Exception as e:
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("list_all_todos", {}, time.time() - start, success=False)
        raise


@tool
def get_todo_details(item_id: str) -> dict:
    """
    Retrieves details of a specific todo.

    :param item_id: The unique ID of the todo item
    :return: Todo details
    """
    return todo_tools.get_todo_details(item_id)


@tool
def create_todo_item(title: str, description: str = "", due_date: str = "") -> dict:
    """
    Creates a new todo item.

    :param title: Todo title (required)
    :param description: Todo description (optional)
    :param due_date: Due date - can be "today", "tomorrow", "next week" or YYYY-MM-DD (optional)
    :return: Created todo information
    """
    print(f"[TOOL CALL] create_todo_item(title={title}, description={description}, due_date={due_date})", file=sys.stderr)
    start = time.time()
    args = {"title": title, "description": description, "due_date": due_date}
    try:
        result = todo_tools.create_todo_item(title=title, description=description, due_date=due_date)
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("create_todo_item", args, time.time() - start, success=True)
        return result
    except Exception as e:
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("create_todo_item", args, time.time() - start, success=False)
        raise


@tool
def update_todo_item(item_id: str, title: str = None, description: str = None, due_date: str = None) -> dict:
    """
    Updates an existing todo item.

    :param item_id: The unique ID of the todo to update
    :param title: New title (optional)
    :param description: New description (optional)
    :param due_date: New due date - can be "today", "tomorrow", etc. (optional)
    :return: Updated todo information
    """
    print(f"[TOOL CALL] update_todo_item(item_id={item_id}, title={title}, description={description}, due_date={due_date})", file=sys.stderr)
    start = time.time()
    args = {"item_id": item_id, "title": title, "description": description, "due_date": due_date}
    try:
        result = todo_tools.update_todo_item(item_id, title, description, due_date)
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("update_todo_item", args, time.time() - start, success=True)
        return result
    except Exception as e:
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("update_todo_item", args, time.time() - start, success=False)
        raise


@tool
def mark_todo_completed(item_id: str) -> dict:
    """
    Marks a todo as completed.

    :param item_id: The unique ID of the todo to mark as completed
    :return: Updated todo with status="completed"
    """
    print(f"[TOOL CALL] mark_todo_completed(item_id={item_id})", file=sys.stderr)
    start = time.time()
    args = {"item_id": item_id}
    try:
        result = todo_tools.mark_todo_completed(item_id)
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("mark_todo_completed", args, time.time() - start, success=True)
        return result
    except Exception as e:
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("mark_todo_completed", args, time.time() - start, success=False)
        raise


@tool
def delete_todo_item(item_id: str) -> dict:
    """
    Deletes a todo item.

    :param item_id: The unique ID of the todo to delete
    :return: Deletion result
    """
    print(f"[TOOL CALL] delete_todo_item(item_id={item_id})", file=sys.stderr)
    start = time.time()
    args = {"item_id": item_id}
    try:
        result = todo_tools.delete_todo_item(item_id)
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("delete_todo_item", args, time.time() - start, success=True)
        return result
    except Exception as e:
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("delete_todo_item", args, time.time() - start, success=False)
        raise


@tool
def search_todos(query: str) -> dict:
    """
    Searches todos using Elasticsearch.

    :param query: Search keyword or phrase (searches in title and description)
    :return: Search results
    """
    print(f"[TOOL CALL] search_todos(query={query})", file=sys.stderr)
    start = time.time()
    args = {"query": query}
    try:
        result = todo_tools.search_todos(query)
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("search_todos", args, time.time() - start, success=True)
        return result
    except Exception as e:
        if os.getenv("AGENT_DEBUG") == "true":
            debug_tracker.track("search_todos", args, time.time() - start, success=False)
        raise
