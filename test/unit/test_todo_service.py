import unittest
from unittest.mock import MagicMock, patch

from src.config.redis_config import ALL_TODOS_KEY, TODO_ITEM_KEY_PREFIX
from src.core.todo_service import TodoService
from src.model.todo_item import TodoItem


class TestTodoService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MagicMock()
        self.patcher = patch("src.core.todo_service.RedisCache")
        self.mock_redis_class = self.patcher.start()
        self.mock_cache = MagicMock()
        self.mock_redis_class.return_value = self.mock_cache
        self.service = TodoService(self.mock_repository)
        self.sample_todo = TodoItem(1, "Sample Todo", "Sample Description", "2025-01-07")

    def tearDown(self):
        self.patcher.stop()

    def test_get_all_todos(self):
        """Test that all todos are retrieved correctly."""
        todos = [
            TodoItem(1, "First Todo", "First Description", "2023-01-01"),
            TodoItem(2, "Second Todo", "Second Description", "2023-01-02"),
        ]

        self.mock_repository.list_all.return_value = todos

        result = self.service.get_all_todos()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "First Todo")
        self.assertEqual(result[1].title, "Second Todo")
        self.mock_repository.list_all.assert_called_once()

    def test_get_todo_by_id_existing(self):
        """Test retrieving a specific todo by ID."""
        self.mock_repository.find_by_id.return_value = self.sample_todo

        result = self.service.get_todo_by_id(1)

        self.assertEqual(result.item_id, 1)
        self.assertEqual(result.title, "Sample Todo")
        self.mock_repository.find_by_id.assert_called_with(1)

    def test_get_todo_by_id_nonexistent(self):
        """Test retrieving a nonexistent todo by ID returns None."""
        self.mock_repository.find_by_id.return_value = None

        result = self.service.get_todo_by_id(999)

        self.assertIsNone(result)
        self.mock_repository.find_by_id.assert_called_with(999)

    def test_create_todo(self):
        """Test creating a new todo."""
        self.mock_repository.todos = []

        result = self.service.create_todo("New Todo", "New Description", "2023-01-01")

        self.assertEqual(result.title, "New Todo")
        self.assertEqual(result.description, "New Description")
        self.assertEqual(result.due_date, "2023-01-01")
        self.assertEqual(result.status, "pending")

        self.mock_repository.add.assert_called_once()

        args, _ = self.mock_repository.add.call_args
        added_todo = args[0]
        self.assertEqual(added_todo.title, "New Todo")
        self.assertEqual(added_todo.description, "New Description")

        self.mock_cache.delete.assert_called_with(ALL_TODOS_KEY)

    def test_update_todo_existing(self):
        """Test updating an existing todo."""
        todo = TodoItem(1, "Test Todo", "Test Description", "2023-01-01")

        self.mock_repository.todos = [todo]

        result = self.service.update_todo(1, title="Updated Title", description="Updated Description")

        self.assertIsNotNone(result)
        self.assertEqual(result, todo)
        self.assertEqual(result.title, "Updated Title")
        self.assertEqual(result.description, "Updated Description")

        self.assertEqual(todo.title, "Updated Title")
        self.assertEqual(todo.description, "Updated Description")

        self.mock_repository._save_to_redis.assert_called_once()

    def test_update_todo_nonexistent(self):
        """Test updating a nonexistent todo returns None."""
        self.mock_repository.todos = []

        result = self.service.update_todo(999, title="Updated Title")

        self.assertIsNone(result)

    def test_mark_as_completed_existing(self):
        """Test marking an existing todo as completed."""
        todo = TodoItem(1, "Test Todo", "Test Description", "2023-01-01", status="completed")

        self.mock_repository.todos = [todo]

        self.service.update_todo = MagicMock(return_value=todo)

        result = self.service.mark_as_completed(1)

        self.assertEqual(result.status, "completed")

        self.service.update_todo.assert_called_with(1, status="completed")

    def test_mark_as_completed_nonexistent(self):
        """Test marking a nonexistent todo as completed returns None."""
        self.mock_repository.todos = []

        result = self.service.mark_as_completed(999)

        self.assertIsNone(result)

    def test_delete_todo_existing(self):
        """Test deleting an existing todo."""
        self.mock_repository.delete.return_value = True

        result = self.service.delete_todo(1)

        self.assertTrue(result)
        self.mock_repository.delete.assert_called_with(1)
        self.mock_cache.delete.assert_any_call(f"{TODO_ITEM_KEY_PREFIX}1")
        self.mock_cache.delete.assert_any_call(ALL_TODOS_KEY)

    def test_delete_todo_nonexistent(self):
        """Test deleting a nonexistent todo returns False."""
        self.mock_repository.delete.return_value = False

        result = self.service.delete_todo(999)

        self.assertFalse(result)
        self.mock_repository.delete.assert_called_with(999)
