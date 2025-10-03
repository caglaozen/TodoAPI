from src.agent import todo_tools as agent_tools


def list_all_todos() -> dict:
    """
    Lists all todo items.

    :return: Todo list with status and count information
    """
    return agent_tools.list_all_todos()


def create_todo(title: str, description: str = "", due_date: str = "") -> dict:
    """
    Creates a new todo item.

    :param title: Todo title (required)
    :param description: Todo description (optional)
    :param due_date: Due date - can be "today", "tomorrow", "next week" or YYYY-MM-DD (optional)
    :return: Created todo information
    """
    return agent_tools.create_todo_item(title=title, description=description, due_date=due_date)


def get_todo_details(item_id: str) -> dict:
    """
    Retrieves details of a specific todo.

    :param item_id: The unique ID of the todo item
    :return: Todo details
    """
    return agent_tools.get_todo_details(item_id)


def update_todo(item_id: str, title: str = None, description: str = None, due_date: str = None) -> dict:
    """
    Updates an existing todo item.

    :param item_id: The unique ID of the todo to update
    :param title: New title (optional)
    :param description: New description (optional)
    :param due_date: New due date - can be "today", "tomorrow", etc. (optional)
    :return: Updated todo information
    """
    return agent_tools.update_todo_item(item_id, title, description, due_date)


def mark_completed(item_id: str) -> dict:
    """
    Marks a todo as completed.

    :param item_id: The unique ID of the todo to mark as completed
    :return: Updated todo with status="completed"
    """
    return agent_tools.mark_todo_completed(item_id)


def delete_todo(item_id: str) -> dict:
    """
    Deletes a todo item.

    :param item_id: The unique ID of the todo to delete
    :return: Deletion result
    """
    return agent_tools.delete_todo_item(item_id)


def search_todos(query: str) -> dict:
    """
    Searches todos using Elasticsearch.

    :param query: Search keyword or phrase (searches in title and description)
    :return: Search results
    """
    return agent_tools.search_todos(query)


def batch_operations(operations: list) -> dict:
    """
    Executes multiple todo operations in a single call.

    :param operations: List of operations, each containing 'action' and 'params'
    :return: Batch operation results
    """
    results = []

    def find_todo_by_title(title: str):
        """Helper to find todo by title (case-insensitive, handles Turkish characters)"""
        all_todos = agent_tools.list_all_todos()
        if all_todos.get("status") == "success":
            search_title = title.lower().strip()
            for todo in all_todos.get("todos", []):
                todo_title = todo.get("title", "").lower().strip()
                if todo_title == search_title:
                    return todo.get("id")
                if todo_title.encode("utf-8").decode("unicode-escape").lower() == search_title:
                    return todo.get("id")
        return None

    for op in operations:
        action = op.get("action")
        params = op.get("params", {})

        try:
            if action == "create":
                result = agent_tools.create_todo_item(
                    title=params.get("title", ""),
                    description=params.get("description", ""),
                    due_date=params.get("due_date", ""),
                )
            elif action == "delete":
                item_id = params.get("item_id") or params.get("title")
                if item_id and not item_id.count("-") >= 4:
                    item_id = find_todo_by_title(item_id)
                if not item_id:
                    result = {
                        "status": "error",
                        "message": f"Todo not found: {params.get('item_id') or params.get('title')}",
                        "deleted": False,
                    }
                else:
                    result = agent_tools.delete_todo_item(item_id)
            elif action == "update":
                item_id = params.get("item_id") or params.get("title")
                if item_id and not item_id.count("-") >= 4:
                    item_id = find_todo_by_title(item_id)
                if not item_id:
                    result = {
                        "status": "error",
                        "message": f"Todo not found: {params.get('item_id') or params.get('title')}",
                        "todo": None,
                    }
                else:
                    result = agent_tools.update_todo_item(
                        item_id=item_id,
                        title=params.get("new_title"),
                        description=params.get("description"),
                        due_date=params.get("due_date"),
                    )
            elif action == "mark_completed":
                item_id = params.get("item_id") or params.get("title")
                if item_id and not item_id.count("-") >= 4:
                    item_id = find_todo_by_title(item_id)
                if not item_id:
                    result = {
                        "status": "error",
                        "message": f"Todo not found: {params.get('item_id') or params.get('title')}",
                        "todo": None,
                    }
                else:
                    result = agent_tools.mark_todo_completed(item_id)
            elif action == "list":
                result = agent_tools.list_all_todos()
            else:
                result = {"status": "error", "message": f"Unknown action: {action}"}

            results.append({"action": action, "result": result})
        except Exception as e:
            results.append({"action": action, "result": {"status": "error", "message": str(e)}})

    return {"status": "success", "message": f"Executed {len(results)} operation(s)", "results": results}
