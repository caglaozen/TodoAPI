import os
import sys
from datetime import datetime, timedelta
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.core.todo_service import TodoService
from src.repository.todo_repository import TodoRepository

_service_instance = None


def get_service() -> TodoService:
    """Returns TodoService singleton instance."""
    global _service_instance
    if _service_instance is None:
        repo = TodoRepository()
        _service_instance = TodoService(repo)
    return _service_instance


def parse_relative_date(date_string: str) -> str:
    """
    Converts relative date expressions to YYYY-MM-DD format.
    Supports both English and Turkish date expressions.

    Args:
        date_string: Date expressions like "today", "tomorrow", "next week",
                    or Turkish equivalents "bugün", "yarın", "gelecek hafta"

    Returns:
        Date in YYYY-MM-DD format
    """
    today = datetime.now()
    date_lower = date_string.lower().strip()

    if date_lower in ["bugün", "today"]:
        return today.strftime("%Y-%m-%d")
    elif date_lower in ["yarın", "tomorrow"]:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_lower in ["gelecek hafta", "next week"]:
        return (today + timedelta(weeks=1)).strftime("%Y-%m-%d")
    elif date_lower in ["bu hafta sonu", "this weekend"]:
        days_until_saturday = (5 - today.weekday()) % 7
        return (today + timedelta(days=days_until_saturday)).strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return date_string
        except:
            return (today + timedelta(days=7)).strftime("%Y-%m-%d")


def list_all_todos() -> dict:
    """
    Lists all todo items.

    Returns:
        dict: Todo list and status information
    """
    try:
        service = get_service()
        todos = service.get_all_todos()

        if not todos:
            return {
                "status": "success",
                "message": "Your todo list is empty. Would you like to add a new todo?",
                "count": 0,
                "todos": [],
            }

        todo_list = []
        for todo in todos:
            todo_list.append(
                {
                    "id": todo.item_id,
                    "title": todo.title,
                    "description": todo.description,
                    "due_date": todo.due_date,
                    "status": todo.status,
                }
            )

        return {
            "status": "success",
            "message": f"Found {len(todos)} todo(s).",
            "count": len(todos),
            "todos": todo_list,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error listing todos: {str(e)}",
            "count": 0,
            "todos": [],
        }


def get_todo_details(item_id: str) -> dict:
    """
    Retrieves details of a specific todo.

    Args:
        item_id: Todo item ID

    Returns:
        dict: Todo details
    """
    try:
        service = get_service()
        todo = service.get_todo_by_id(item_id)

        if not todo:
            return {
                "status": "error",
                "message": f"Todo with ID '{item_id}' not found.",
                "todo": None,
            }

        return {
            "status": "success",
            "message": "Todo details retrieved successfully.",
            "todo": {
                "id": todo.item_id,
                "title": todo.title,
                "description": todo.description,
                "due_date": todo.due_date,
                "status": todo.status,
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving todo details: {str(e)}",
            "todo": None,
        }


def create_todo_item(title: str, description: str = "", due_date: str = "") -> dict:
    """
    Creates a new todo item.

    Args:
        title: Todo title (required)
        description: Todo description (optional)
        due_date: Due date - relative expressions like "today", "tomorrow" or YYYY-MM-DD format (optional)

    Returns:
        dict: Created todo information
    """
    try:
        if not due_date:
            parsed_date = parse_relative_date("next week")
        else:
            parsed_date = parse_relative_date(due_date)

        service = get_service()
        todo = service.create_todo(title=title, description=description or "", due_date=parsed_date)

        return {
            "status": "success",
            "message": f"Todo '{title}' created successfully! Due date: {parsed_date}",
            "todo": {
                "id": todo.item_id,
                "title": todo.title,
                "description": todo.description,
                "due_date": todo.due_date,
                "status": todo.status,
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating todo: {str(e)}",
            "todo": None,
        }


def update_todo_item(
    item_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
) -> dict:
    """
    Updates an existing todo item.

    Args:
        item_id: ID of the todo to update
        title: New title (optional)
        description: New description (optional)
        due_date: New due date (optional)

    Returns:
        dict: Updated todo information
    """
    try:
        updates = {}
        if title:
            updates["title"] = title
        if description:
            updates["description"] = description
        if due_date:
            updates["due_date"] = parse_relative_date(due_date)

        if not updates:
            return {
                "status": "error",
                "message": "No fields specified for update.",
                "todo": None,
            }

        service = get_service()
        todo = service.update_todo(item_id, **updates)

        if not todo:
            return {
                "status": "error",
                "message": f"Todo with ID '{item_id}' not found.",
                "todo": None,
            }

        return {
            "status": "success",
            "message": f"Todo '{todo.title}' updated successfully.",
            "todo": {
                "id": todo.item_id,
                "title": todo.title,
                "description": todo.description,
                "due_date": todo.due_date,
                "status": todo.status,
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error updating todo: {str(e)}",
            "todo": None,
        }


def mark_todo_completed(item_id: str) -> dict:
    """
    Marks a todo as completed.

    Args:
        item_id: ID of the todo to mark as completed

    Returns:
        dict: Updated todo information
    """
    try:
        service = get_service()
        todo = service.mark_as_completed(item_id)

        if not todo:
            return {
                "status": "error",
                "message": f"Todo with ID '{item_id}' not found.",
                "todo": None,
            }

        return {
            "status": "success",
            "message": f"✅ Todo '{todo.title}' marked as completed!",
            "todo": {
                "id": todo.item_id,
                "title": todo.title,
                "description": todo.description,
                "due_date": todo.due_date,
                "status": todo.status,
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error completing todo: {str(e)}",
            "todo": None,
        }


def delete_todo_item(item_id: str) -> dict:
    """
    Deletes a todo item.

    Args:
        item_id: ID of the todo to delete

    Returns:
        dict: Deletion result
    """
    try:
        service = get_service()

        todo = service.get_todo_by_id(item_id)
        if not todo:
            return {
                "status": "error",
                "message": f"Todo with ID '{item_id}' not found.",
                "deleted": False,
            }

        title = todo.title
        result = service.delete_todo(item_id)

        if result:
            return {
                "status": "success",
                "message": f"🗑️ Todo '{title}' deleted successfully.",
                "deleted": True,
            }
        else:
            return {
                "status": "error",
                "message": "Error occurred while deleting todo.",
                "deleted": False,
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error deleting todo: {str(e)}",
            "deleted": False,
        }


def search_todos(query: str) -> dict:
    """
    Searches todos using Elasticsearch.

    Args:
        query: Search keyword or phrase

    Returns:
        dict: Search results
    """
    try:
        service = get_service()
        results = service.es_client.search_todos(query)
        hits = results["hits"]["hits"]

        if not hits:
            return {
                "status": "success",
                "message": f"No results found for '{query}'.",
                "count": 0,
                "todos": [],
            }

        todo_list = [hit["_source"] for hit in hits]

        return {
            "status": "success",
            "message": f"Found {len(hits)} result(s) for '{query}'.",
            "count": len(hits),
            "todos": todo_list,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error searching todos: {str(e)}",
            "count": 0,
            "todos": [],
        }
