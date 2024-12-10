class TodoRepository:
    def __init__(self):
        """
        Initialize the TodoRepository with an empty list of todos.
        """
        self.todos = []

    def add(self, todo):
        """
        Adds a new TodoItem to the repository.

        :param todo: The TodoItem instance to add.
        """
        self.todos.append(todo)

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
            return True
        return False

    def list_all(self):
        """
        Lists all TodoItems in the repository.

        :return: A list of all TodoItem instances in the repository.
        """
        return self.todos
