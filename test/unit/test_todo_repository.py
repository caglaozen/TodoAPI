import json
import os
import unittest

from src.model.todo_item import TodoItem
from src.repository.todo_repository import TodoRepository


class TestTodoRepository(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "test_todos.json"
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
        self.repository = TodoRepository(file_path=self.test_file_path)
        self.sample_todo = TodoItem(
            item_id=1, title="Sample Todo", description="Sample Description", due_date="2025-01-07"
        )

    def tearDown(self):
        os.remove(self.test_file_path)

    def test_add(self):
        """
        Test that a new TodoItem is added to the repository and saved to a file.
        """
        todo = TodoItem(item_id=1, title="Test Add", description="Adding a test todo", due_date="2025-01-07")
        self.repository.add(todo)

        self.assertEqual(len(self.repository.todos), 1)
        self.assertEqual(self.repository.todos[0].title, "Test Add")
        self.assertTrue(os.path.exists(self.test_file_path))

        with open(self.test_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["title"], "Test Add")

    def test_find_by_id(self):
        """
        Test that a TodoItem can be found by its ID.
        """
        self.repository.todos = [self.sample_todo]

        found_todo = self.repository.find_by_id(1)
        self.assertEqual(found_todo, self.sample_todo)

        not_found_todo = self.repository.find_by_id(2)
        self.assertIsNone(not_found_todo)

    def test_add_duplicate_id(self):
        """
        Test that adding a TodoItem with a duplicate ID raises a ValueError.
        """
        self.repository.add(self.sample_todo)
        duplicate_todo = TodoItem(
            item_id=1, title="Duplicate Todo", description="Duplicate Description", due_date="2025-01-08"
        )
        with self.assertRaises(ValueError) as context:
            self.repository.add(duplicate_todo)
        self.assertEqual(str(context.exception), "A TodoItem with ID 1 already exists.")

    def test_delete(self):
        """
        Test that a TodoItem is deleted from the repository and removed from the file.
        """
        self.repository.todos = [self.sample_todo]

        self.assertTrue(self.repository.delete(1))
        self.assertEqual(len(self.repository.todos), 0)

        with open(self.test_file_path, "r") as file:
            data = json.load(file)
            self.assertEqual(len(data), 0)

        self.assertFalse(self.repository.delete(2))

    def test_list_all(self):
        """
        Test that all TodoItems are listed correctly from the repository.
        """
        todo_1 = TodoItem(item_id=2, title="Second Todo", description="Another Description", due_date="2025-01-07")
        self.repository.todos = [self.sample_todo, todo_1]

        todos = self.repository.list_all()
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0].title, "Sample Todo")
        self.assertEqual(todos[1].title, "Second Todo")

    def test_save_to_file(self):
        """
        Test that the list of TodoItems is saved to a file.
        """
        self.repository.todos = [self.sample_todo]
        self.repository.save_to_file()

        with open(self.test_file_path, "r") as file:
            data = json.load(file)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["item_id"], 1)
            self.assertEqual(data[0]["title"], "Sample Todo")
            self.assertEqual(data[0]["description"], "Sample Description")
            self.assertEqual(data[0]["due_date"], "2025-01-07")

    def test_load_from_file(self):
        """
        Test that TodoItems are loaded from the file if it exists.
        """
        with open(self.test_file_path, "w", encoding="utf-8") as file:
            json.dump([self.sample_todo.__dict__], file)

        todos = self.repository._load_from_file()
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].item_id, 1)
        self.assertEqual(todos[0].title, "Sample Todo")
        self.assertEqual(todos[0].description, "Sample Description")
        self.assertEqual(todos[0].due_date, "2025-01-07")
