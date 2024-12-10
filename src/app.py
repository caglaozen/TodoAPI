from flask import Flask, jsonify, request

from src.core.todo_service import TodoService
from src.repository.todo_repository import TodoRepository

app = Flask(__name__)

repo = TodoRepository()
service = TodoService(repo)


@app.route("/todos", methods=["POST"])
def create_todo():
    """
    Handles the POST request to create a new todo item.

    :return: A JSON response containing the created TodoItem details.
    """
    data = request.json

    todo = service.create_todo(
        title=data["title"],
        description=data["description"],
        due_date=data["due_date"]
    )

    return jsonify(
        {
            "item_id": todo.item_id,
            "title": todo.title,
            "description": todo.description,
            "due_date": todo.due_date,
            "status": todo.status
        }
    ), 201


@app.route("/todos/<int:item_id>", methods=["PUT"])
def update_todo(item_id):
    """
    Handles the PUT request to update a specific todo item.

    :param item_id: The ID of the todo item to update.
    :return: A JSON response containing the updated TodoItem details or 404 status code if the item does not exist.
    """
    data = request.json

    todo = service.update_todo(
        item_id,
        title=data.get("title"),
        description=data.get("description"),
        due_date=data.get("due_date"),
        status=data.get("status")
    )

    if todo is None:
        return jsonify({"message": "Todo item not found"}), 404

    return jsonify(
        {
            "item_id": todo.item_id,
            "title": todo.title,
            "description": todo.description,
            "due_date": todo.due_date,
            "status": todo.status
        }
    ), 200


@app.route("/todos/<int:item_id>", methods=["DELETE"])
def delete_todo(item_id):
    """
    Handles the DELETE request to delete a specific todo item.

    :param item_id: The ID of the todo item to delete.
    :return: A JSON response with a success message or 404 status code if the item does not exist.
    """
    if service.delete_todo(item_id):
        return jsonify({"message": "Todo item deleted"}), 200
    else:
        return jsonify({"message": "Todo item not found"}), 404


@app.route("/todos", methods=["GET"])
def list_all_todos():
    """
    Handles the GET request to list all todo items.

    :return: A JSON response containing a list of all TodoItem details and a 200 status code.
    """
    todos = service.repository.list_all()

    result = [
        {
            "item_id": todo.item_id,
            "title": todo.title,
            "description": todo.description,
            "due_date": todo.due_date,
            "status": todo.status
        }
        for todo in todos
    ]

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)
