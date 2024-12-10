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
