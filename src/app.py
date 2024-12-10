from flask import Flask, jsonify, request

from src.core.todo_service import TodoService
from src.repository.todo_repository import TodoRepository

app = Flask(__name__)

repo = TodoRepository()
service = TodoService(repo)


@app.route("/todos", methods=["POST"])
def create_todo():
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


@app.route("/todos", methods=["GET"])
def list_all_todos():
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
