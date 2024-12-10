import uuid

from src.model.todo_item import TodoItem


class TodoService:
    def __init__(self, repository):
        self.repository = repository

    def create_todo(self, title, description, due_date):
        todo = TodoItem(len(self.repository.todos) + 1, title, description, due_date)
        self.repository.add(todo)
        return todo
