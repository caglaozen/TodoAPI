class TodoRepository:
    def __init__(self):
        self.todos = []

    def add(self, todo):
        self.todos.append(todo)

    def list_all(self):
        return self.todos
