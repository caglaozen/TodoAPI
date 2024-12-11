from src.model.todo_item import TodoItem


class TodoService:
    def __init__(self, repository):
        """
        Initializes the TodoService with a repository to manage TodoItems.

        :param repository: A repository object that manages TodoItem instances.
        """
        self.repository = repository

    def create_todo(self, title, description, due_date):
        """
        Creates a new TodoItem with the given details and adds it to the repository.

        :param title: The title of the TodoItem.
        :param description: A brief description of the TodoItem.
        :param due_date: The due date of the TodoItem.
        :return: The created TodoItem instance.
        """
        todo = TodoItem(len(self.repository.todos) + 1, title, description, due_date)
        self.repository.add(todo)
        return todo

    def update_todo(self, item_id, **updates):
        """
        Updates an existing TodoItem with the given details.

        :param item_id: The ID of the todo item to update.
        :param updates: The details to update for the TodoItem.
        :return: The updated TodoItem instance, or None if the item does not exist.
        """
        for todo in self.repository.todos:
            if todo.item_id == item_id:
                valid_fields = {
                    key: value for key, value in updates.items() if value is not None and hasattr(todo, key)
                }
                for key, value in valid_fields.items():
                    setattr(todo, key, value)
                return todo
        return None

    def delete_todo(self, item_id):
        """
        Deletes an existing TodoItem with the given ID.

        :param item_id: The ID of the todo item to delete.
        :return: True if the item was deleted, False otherwise.
        """
        return self.repository.delete(item_id)
