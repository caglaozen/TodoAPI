import json
import os.path

from src.model.todo_item import TodoItem


class TodoRepository:
    def __init__(self, file_path="src/outputs/todos.json"):
        """
        Initialize the TodoRepository with an empty list of todos.
        """
        self.file_path = file_path
        self.todos = self._load_from_file()

    def _load_from_file(self):
        """
        Loads todos from a JSON file if it exists.

        :return: A list of TodoItem instances.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return [TodoItem(**item) for item in data]
        return []

    def _save_to_file(self):
        """
        Saves the current list of todos to a JSON file.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([todo.__dict__ for todo in self.todos], file, ensure_ascii=False, indent=4)

    def add(self, todo):
        """
        Adds a new TodoItem to the repository.

        :param todo: The TodoItem instance to add.
        """
        self.todos.append(todo)
        self._save_to_file()

    def find_by_id(self, item_id):
        """
        Finds a TodoItem by its ID.

        :param item_id: The ID of the TodoItem to find.
        """
        return next((todo for todo in self.todos if todo.item_id == item_id), None)

    def delete(self, item_id):
        """
        Deletes a TodoItem by its ID.

        :param item_id: The ID of the TodoItem to delete.
        """
        todo = self.find_by_id(item_id)
        if todo:
            self.todos.remove(todo)
            self._save_to_file()
            return True
        return False

    def list_all(self):
        """
        Lists all TodoItems in the repository.

        :return: A list of all TodoItem instances in the repository.
        """
        return self.todos
