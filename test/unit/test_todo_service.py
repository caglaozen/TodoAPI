import unittest

from src.core.todo_service import TodoService
from src.repository.todo_repository import TodoRepository


class TestTodoService(unittest.TestCase):
    def setUp(self):
        self.repository = TodoRepository()
        self.service = TodoService(self.repository)
        self.repository.todos.clear()

    def test_create_todo(self):
        """
        Test that a new TodoItem is created and added to the repository.
        """
        todo = self.service.create_todo("Test Title", "Test Description", "2024-11-03")
        self.assertEqual(todo.title, "Test Title")
        self.assertEqual(todo.description, "Test Description")
        self.assertEqual(todo.due_date, "2024-11-03")
        self.assertEqual(len(self.repository.todos), 1)

    def test_update_todo(self):
        """
        Test that an existing TodoItem is updated with the new details.
        """
        todo = self.service.create_todo("Test Title", "Test Description", "2024-11-03")
        updated_todo = self.service.update_todo(
            todo.item_id, title="Updated Title", description="Updated Description", due_date="2024-11-04"
        )
        self.assertIsNotNone(updated_todo)
        self.assertEqual(updated_todo.title, "Updated Title")
        self.assertEqual(updated_todo.description, "Updated Description")
        self.assertEqual(updated_todo.due_date, "2024-11-04")

        non_existent_update = self.service.update_todo(999, title="Non-existent Title")
        self.assertIsNone(non_existent_update)

    def test_delete_todo(self):
        """
        Test that an existing TodoItem is deleted from the repository.
        """
        todo = self.service.create_todo("Test Title", "Test Description", "2024-11-03")
        self.assertTrue(self.service.delete_todo(todo.item_id))
        self.assertEqual(len(self.repository.todos), 0)

        self.assertFalse(self.service.delete_todo(999))

    def test_list_all_todos(self):
        """
        Test that all TodoItems are listed from the repository.
        """
        todo_1 = self.service.create_todo("Test Title 1", "Test Description 1", "2024-11-03")
        todo_2 = self.service.create_todo("Test Title 2", "Test Description 2", "2024-11-04")

        todos = self.repository.list_all()
        self.assertEqual(len(todos), 2)
        self.assertEqual(todo_1.title, "Test Title 1")
        self.assertEqual(todo_2.title, "Test Title 2")
        self.assertEqual(todo_1.description, "Test Description 1")
        self.assertEqual(todo_2.description, "Test Description 2")
        self.assertEqual(todo_1.due_date, "2024-11-03")
        self.assertEqual(todo_2.due_date, "2024-11-04")
        self.assertEqual(todo_1.status, "pending")
        self.assertEqual(todo_2.status, "pending")
