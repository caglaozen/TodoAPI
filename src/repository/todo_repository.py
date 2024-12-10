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

    def list_all(self):
        """
        Lists all TodoItems in the repository.

        :return: A list of all TodoItem instances in the repository.
        """
        return self.todos
