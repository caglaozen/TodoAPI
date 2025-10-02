import unittest
from unittest.mock import MagicMock, patch

from src.config.redis_config import ALL_TODOS_KEY, TODO_ITEM_KEY_PREFIX
from src.model.todo_item import TodoItem
from src.repository.todo_repository import TodoRepository


class TestTodoRepository(unittest.TestCase):
    def setUp(self):
        self.mock_cache = MagicMock()
        self.patcher = patch("src.repository.todo_repository.RedisCache", return_value=self.mock_cache)
        self.mock_redis_class = self.patcher.start()
        self.repository = TodoRepository()
        self.repository.todos = []
        self.sample_todo = TodoItem(1, "Sample Todo", "Sample Description", "2025-01-07")

    def tearDown(self):
        self.patcher.stop()

    def test_add_todo(self):
        """Test that a new TodoItem is added to the repository and saved to Redis."""
        todo = TodoItem(1, "Test Title", "Test Description", "2023-01-01")

        self.mock_cache.get.return_value = None
        self.repository.add(todo)

        self.mock_cache.set.assert_any_call("all_todos", [todo])
        self.mock_cache.set.assert_any_call(f"todo_{todo.item_id}", todo)

    def test_find_by_id_existing(self):
        """Test that a TodoItem can be found by its ID."""
        todo_dict = self.sample_todo.__dict__
        self.mock_cache.get.return_value = todo_dict

        found_todo = self.repository.find_by_id(1)

        self.assertEqual(found_todo.item_id, 1)
        self.assertEqual(found_todo.title, "Sample Todo")
        self.mock_cache.get.assert_called_with("todo_1")

    def test_find_by_id_nonexisting(self):
        """Test that finding a non-existent TodoItem returns None."""
        self.mock_cache.get.return_value = None

        result = self.repository.find_by_id(999)

        self.assertIsNone(result)
        self.mock_cache.get.assert_called_with("todo_999")

    def test_add_duplicate_id(self):
        """Test that adding a TodoItem with a duplicate ID raises a ValueError."""
        self.repository.todos = [self.sample_todo]

        self.mock_cache.get.return_value = self.sample_todo.__dict__

        duplicate_todo = TodoItem(1, "Duplicate Todo", "Duplicate Description", "2025-01-08")

        with self.assertRaises(ValueError) as context:
            self.repository.add(duplicate_todo)

        self.assertEqual(str(context.exception), "A TodoItem with ID 1 already exists.")

    def test_delete_existing(self):
        """Test that a TodoItem is deleted from the repository and removed from Redis."""
        todo = TodoItem(1, "Sample Todo", "Sample Description", "2025-01-07")

        self.repository.todos = [todo]

        self.repository.find_by_id = MagicMock(return_value=todo)

        self.mock_cache.get.return_value = None

        result = self.repository.delete(1)

        self.assertTrue(result)
        self.assertEqual(len(self.repository.todos), 0)  # Verify item was removed from list
        self.mock_cache.delete.assert_any_call(f"{TODO_ITEM_KEY_PREFIX}1")
        self.mock_cache.delete.assert_any_call(ALL_TODOS_KEY)

    def test_delete_nonexisting(self):
        """Test that deleting a non-existent TodoItem returns False."""
        self.mock_cache.get.return_value = None

        result = self.repository.delete(999)

        self.assertFalse(result)

    def test_list_all(self):
        """Test that all TodoItems are listed correctly from Redis."""
        todos_data = [
            {
                "item_id": 1,
                "title": "First Todo",
                "description": "First Description",
                "due_date": "2023-01-01",
                "status": "pending",
            },
            {
                "item_id": 2,
                "title": "Second Todo",
                "description": "Second Description",
                "due_date": "2023-01-02",
                "status": "completed",
            },
        ]

        self.mock_cache.get.return_value = todos_data

        todos = self.repository.list_all()

        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0].title, "First Todo")
        self.assertEqual(todos[1].title, "Second Todo")
        self.mock_cache.get.assert_called_with("all_todos")

    def test_load_from_redis(self):
        """Test that TodoItems are loaded from Redis correctly."""
        todos_data = [
            {
                "item_id": 1,
                "title": "Test Todo",
                "description": "Test Description",
                "due_date": "2023-01-01",
                "status": "pending",
            }
        ]

        self.mock_cache.get.return_value = todos_data

        todos = self.repository._load_from_redis()

        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].item_id, 1)
        self.assertEqual(todos[0].title, "Test Todo")
        self.mock_cache.get.assert_called_with("all_todos")

    def test_save_to_redis(self):
        """Test that TodoItems are saved to Redis correctly."""
        self.repository.todos = [self.sample_todo]

        self.repository._save_to_redis()

        self.mock_cache.set.assert_any_call(ALL_TODOS_KEY, [self.sample_todo])

        self.mock_cache.set.assert_any_call(f"{TODO_ITEM_KEY_PREFIX}{self.sample_todo.item_id}", self.sample_todo)

    def test_find_by_id_in_repository_list(self):
        """Test finding a todo by ID in repository list when not cached."""
        todo = TodoItem(1, "Test Todo", "Test Description", "2023-01-01")
        self.repository.todos = [todo]
        self.mock_cache.get.return_value = None

        found_todo = self.repository.find_by_id(1)

        self.assertEqual(found_todo.item_id, 1)
        self.assertEqual(found_todo.title, "Test Todo")
        self.mock_cache.set.assert_called_with(f"{TODO_ITEM_KEY_PREFIX}1", todo)

    def test_list_all_empty_cache(self):
        """Test list_all when cache is empty."""
        self.mock_cache.get.return_value = None
        todo = TodoItem(1, "Test Todo", "Test Description", "2023-01-01")
        self.repository.todos = [todo]

        result = self.repository.list_all()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Test Todo")
        # Verify that both ALL_TODOS_KEY and individual todo were cached
        self.mock_cache.set.assert_any_call(ALL_TODOS_KEY, [todo])
        self.mock_cache.set.assert_any_call(f"{TODO_ITEM_KEY_PREFIX}1", todo)

    def test_load_from_redis_empty(self):
        """Test loading from Redis when cache is empty."""
        self.mock_cache.get.return_value = None

        todos = self.repository._load_from_redis()

        self.assertEqual(len(todos), 0)

    def test_update_existing_todo(self):
        """Test updating an existing todo."""
        todo = TodoItem(1, "Original Title", "Original Description", "2023-01-01")
        self.repository.todos = [todo]

        updated_todo = self.repository.update(1, title="Updated Title", description="Updated Description")

        self.assertIsNotNone(updated_todo)
        self.assertEqual(updated_todo.title, "Updated Title")
        self.assertEqual(updated_todo.description, "Updated Description")
        self.mock_cache.set.assert_called()

    def test_update_nonexistent_todo(self):
        """Test updating a non-existent todo returns None."""
        self.repository.todos = []

        result = self.repository.update(999, title="Updated Title")

        self.assertIsNone(result)

    def test_update_with_none_values(self):
        """Test updating a todo with None values (should be ignored)."""
        todo = TodoItem(1, "Original Title", "Original Description", "2023-01-01")
        self.repository.todos = [todo]

        updated_todo = self.repository.update(1, title=None, description="New Description")

        self.assertEqual(updated_todo.title, "Original Title")
        self.assertEqual(updated_todo.description, "New Description")

    def test_update_with_invalid_fields(self):
        """Test updating a todo with invalid field names (should be ignored)."""
        todo = TodoItem(1, "Original Title", "Original Description", "2023-01-01")
        self.repository.todos = [todo]

        updated_todo = self.repository.update(1, invalid_field="value", title="New Title")

        self.assertEqual(updated_todo.title, "New Title")
        self.assertFalse(hasattr(updated_todo, "invalid_field"))
