import unittest

from src.core.todo_service import TodoService
from src.repository.todo_repository import TodoRepository


class TestTodoService(unittest.TestCase):
    def setUp(self):
        self.repository = TodoRepository()
        self.service = TodoService(self.repository)

    def test_create_todo(self):
        """
        Test that a new TodoItem is created and added to the repository.
        """
        todo = self.service.create_todo("Test Title", "Test Description", "2024-11-03")
        self.assertEqual(todo.title, "Test Title")
        self.assertEqual(todo.description, "Test Description")
        self.assertEqual(todo.due_date, "2024-11-03")
        self.assertEqual(len(self.repository.todos), 1)

    def test_list_all_todos(self):
        """
        Test that all TodoItems are listed from the repository.
        """
        todo_1 = self.service.create_todo("Test Title 1", "Test Description 1", "2024-11-03")
        todo_2 = self.service.create_todo("Test Title 2", "Test Description 2", "2024-11-04")

        todos = self.repository.list_all()
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0].title, "Test Title 1")
        self.assertEqual(todos[1].title, "Test Title 2")
        self.assertEqual(todos[0].description, "Test Description 1")
        self.assertEqual(todos[1].description, "Test Description 2")
        self.assertEqual(todos[0].due_date, "2024-11-03")
        self.assertEqual(todos[1].due_date, "2024-11-04")
        self.assertEqual(todos[0].status, "pending")
        self.assertEqual(todos[1].status, "pending")
