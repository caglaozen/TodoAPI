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
