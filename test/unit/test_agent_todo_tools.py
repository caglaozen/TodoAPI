import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

sys.modules["google"] = MagicMock()
sys.modules["google.adk"] = MagicMock()
sys.modules["google.adk.agents"] = MagicMock()

from src.agent import todo_tools
from src.model.todo_item import TodoItem


class TestAgentTodoTools(unittest.TestCase):
    @patch("src.agent.todo_tools.get_service")
    def test_list_all_todos_success(self, mock_get_service):
        """Test listing all todos successfully."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        todos = [
            TodoItem(1, "Test Todo 1", "Description 1", "2025-01-01"),
            TodoItem(2, "Test Todo 2", "Description 2", "2025-01-02"),
        ]
        mock_service.get_all_todos.return_value = todos

        result = todo_tools.list_all_todos()

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["count"], 2)
        self.assertEqual(len(result["todos"]), 2)
        self.assertEqual(result["todos"][0]["title"], "Test Todo 1")

    @patch("src.agent.todo_tools.get_service")
    def test_list_all_todos_empty(self, mock_get_service):
        """Test listing todos when list is empty."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.get_all_todos.return_value = []

        result = todo_tools.list_all_todos()

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["message"], "Your todo list is empty. Would you like to add a new todo?")

    @patch("src.agent.todo_tools.get_service")
    def test_list_all_todos_error(self, mock_get_service):
        """Test listing todos with error."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.get_all_todos.side_effect = Exception("Database error")

        result = todo_tools.list_all_todos()

        self.assertEqual(result["status"], "error")
        self.assertIn("Error listing todos", result["message"])

    @patch("src.agent.todo_tools.get_service")
    def test_get_todo_details_success(self, mock_get_service):
        """Test getting todo details successfully."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        todo = TodoItem(1, "Test Todo", "Test Description", "2025-01-01")
        mock_service.get_todo_by_id.return_value = todo

        result = todo_tools.get_todo_details("1")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["todo"]["title"], "Test Todo")

    @patch("src.agent.todo_tools.get_service")
    def test_get_todo_details_not_found(self, mock_get_service):
        """Test getting todo details when not found."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.get_todo_by_id.return_value = None

        result = todo_tools.get_todo_details("999")

        self.assertEqual(result["status"], "error")
        self.assertIn("not found", result["message"])

    @patch("src.agent.todo_tools.get_service")
    def test_create_todo_item_success(self, mock_get_service):
        """Test creating a todo item successfully."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        todo = TodoItem(1, "New Todo", "New Description", "2025-01-08")
        mock_service.create_todo.return_value = todo

        result = todo_tools.create_todo_item("New Todo", "New Description", "tomorrow")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["todo"]["title"], "New Todo")
        self.assertIn("created successfully", result["message"])

    @patch("src.agent.todo_tools.get_service")
    def test_create_todo_item_default_due_date(self, mock_get_service):
        """Test creating a todo with default due date (next week)."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        expected_date = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")
        todo = TodoItem(1, "New Todo", "", expected_date)
        mock_service.create_todo.return_value = todo

        result = todo_tools.create_todo_item("New Todo")

        self.assertEqual(result["status"], "success")
        mock_service.create_todo.assert_called_once()

    @patch("src.agent.todo_tools.get_service")
    def test_create_todo_item_error(self, mock_get_service):
        """Test creating todo with error."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.create_todo.side_effect = Exception("Creation error")

        result = todo_tools.create_todo_item("New Todo")

        self.assertEqual(result["status"], "error")
        self.assertIn("Error creating todo", result["message"])

    @patch("src.agent.todo_tools.get_service")
    def test_update_todo_item_success(self, mock_get_service):
        """Test updating a todo item successfully."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        todo = TodoItem(1, "Updated Todo", "Updated Description", "2025-01-10")
        mock_service.update_todo.return_value = todo

        result = todo_tools.update_todo_item("1", title="Updated Todo", description="Updated Description")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["todo"]["title"], "Updated Todo")

    @patch("src.agent.todo_tools.get_service")
    def test_update_todo_item_not_found(self, mock_get_service):
        """Test updating a non-existent todo."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.update_todo.return_value = None

        result = todo_tools.update_todo_item("999", title="Updated")

        self.assertEqual(result["status"], "error")
        self.assertIn("not found", result["message"])

    def test_update_todo_item_no_fields(self):
        """Test updating todo with no fields specified."""
        result = todo_tools.update_todo_item("1")

        self.assertEqual(result["status"], "error")
        self.assertIn("No fields specified", result["message"])

    @patch("src.agent.todo_tools.get_service")
    def test_mark_todo_completed_success(self, mock_get_service):
        """Test marking a todo as completed successfully."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        todo = TodoItem(1, "Test Todo", "Test Description", "2025-01-01", status="completed")
        mock_service.mark_as_completed.return_value = todo

        result = todo_tools.mark_todo_completed("1")

        self.assertEqual(result["status"], "success")
        self.assertIn("marked as completed", result["message"])

    @patch("src.agent.todo_tools.get_service")
    def test_mark_todo_completed_not_found(self, mock_get_service):
        """Test marking a non-existent todo as completed."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.mark_as_completed.return_value = None

        result = todo_tools.mark_todo_completed("999")

        self.assertEqual(result["status"], "error")
        self.assertIn("not found", result["message"])

    @patch("src.agent.todo_tools.get_service")
    def test_delete_todo_item_success(self, mock_get_service):
        """Test deleting a todo item successfully."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        todo = TodoItem(1, "Test Todo", "Test Description", "2025-01-01")
        mock_service.get_todo_by_id.return_value = todo
        mock_service.delete_todo.return_value = True

        result = todo_tools.delete_todo_item("1")

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["deleted"])
        self.assertIn("deleted successfully", result["message"])

    @patch("src.agent.todo_tools.get_service")
    def test_delete_todo_item_not_found(self, mock_get_service):
        """Test deleting a non-existent todo."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.get_todo_by_id.return_value = None

        result = todo_tools.delete_todo_item("999")

        self.assertEqual(result["status"], "error")
        self.assertFalse(result["deleted"])
        self.assertIn("not found", result["message"])

    @patch("src.agent.todo_tools.get_service")
    def test_delete_todo_item_deletion_failed(self, mock_get_service):
        """Test when deletion operation fails."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        todo = TodoItem(1, "Test Todo", "Test Description", "2025-01-01")
        mock_service.get_todo_by_id.return_value = todo
        mock_service.delete_todo.return_value = False

        result = todo_tools.delete_todo_item("1")

        self.assertEqual(result["status"], "error")
        self.assertFalse(result["deleted"])

    @patch("src.agent.todo_tools.get_service")
    def test_search_todos_success(self, mock_get_service):
        """Test searching todos successfully."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.es_client.search_todos.return_value = {
            "hits": {
                "hits": [
                    {"_source": {"item_id": 1, "title": "Test Todo", "description": "Test"}},
                    {"_source": {"item_id": 2, "title": "Another Test", "description": "Test"}},
                ]
            }
        }

        result = todo_tools.search_todos("test")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["count"], 2)
        self.assertEqual(len(result["todos"]), 2)

    @patch("src.agent.todo_tools.get_service")
    def test_search_todos_no_results(self, mock_get_service):
        """Test searching todos with no results."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.es_client.search_todos.return_value = {"hits": {"hits": []}}

        result = todo_tools.search_todos("nonexistent")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["message"], "No results found for 'nonexistent'.")

    @patch("src.agent.todo_tools.get_service")
    def test_search_todos_error(self, mock_get_service):
        """Test searching todos with error."""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_service.es_client.search_todos.side_effect = Exception("Search error")

        result = todo_tools.search_todos("test")

        self.assertEqual(result["status"], "error")
        self.assertIn("Error searching todos", result["message"])
